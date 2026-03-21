"""
Given 5 SQL candidates from Vanna, score and rank them.
Pick the best one for execution.
"""
import re
import sqlglot
from guardrails.output_guard import check_sql

DESIRED_TABLES = {
    "energy": ["interval_raw", "daily_raw"],
    "events": ["event_raw"],
    "device": ["device"],
    "load": ["interval_raw", "daily_raw"],
    "voltage": ["interval_raw", "instant_raw"],
    "current": ["interval_raw", "instant_raw"],
}

def score_sql(sql: str, intent_keywords: list[str]) -> dict:
    """
    Score a single SQL string on multiple dimensions.
    Returns {sql, score, details, valid}
    """
    score = 0
    details = []

    # 1. Guard check (disqualify if fails)
    guard = check_sql(sql)
    if not guard.allowed:
        return {"sql": sql, "score": -1, "details": [guard.reason], "valid": False}

    sql_lower = sql.lower()

    # 2. Syntax validity via sqlglot
    try:
        sqlglot.parse_one(sql, dialect="postgres")
        score += 20
        details.append("+20: Valid SQL syntax")
    except Exception as e:
        return {"sql": sql, "score": -1, "details": [f"Syntax error: {e}"], "valid": False}

    # 3. Uses expected tables for the query intent
    for intent, tables in DESIRED_TABLES.items():
        if intent in intent_keywords:
            for t in tables:
                if t in sql_lower:
                    score += 15
                    details.append(f"+15: Uses {t} for {intent}")

    # 4. Has time filter (important for performance + correctness)
    time_cols = ["interval_end_time", "event_time", "read_time", "insert_ts"]
    has_time_filter = any(col in sql_lower for col in time_cols)
    if has_time_filter:
        score += 20
        details.append("+20: Has time boundary filter")
    else:
        score -= 10
        details.append("-10: No time filter — may scan entire table")

    # 5. Has device_id filter
    if "device_id" in sql_lower:
        score += 15
        details.append("+15: Has device_id filter")

    # 6. Aggregation present (summary queries should aggregate)
    agg_fns = ["sum(", "avg(", "max(", "min(", "count("]
    if any(fn in sql_lower for fn in agg_fns):
        score += 10
        details.append("+10: Has aggregation")

    # 7. No SELECT * (prefer explicit columns)
    if "select *" not in sql_lower:
        score += 5
        details.append("+5: No SELECT *")

    # 8. Has ORDER BY (structured output)
    if "order by" in sql_lower:
        score += 5
        details.append("+5: Has ORDER BY")

    # 9. Penalise very short SQL (probably incomplete)
    if len(sql.strip()) < 80:
        score -= 15
        details.append("-15: SQL suspiciously short")

    # 10. Penalise CROSS JOIN without condition (accidental cartesian)
    if "cross join" in sql_lower and "where" not in sql_lower:
        score -= 20
        details.append("-20: CROSS JOIN without WHERE")

    return {"sql": sql, "score": score, "details": details, "valid": True}

def rank_sql_candidates(
    candidates: list[str],
    intent_keywords: list[str],
) -> tuple[str, list[dict]]:
    """
    Rank all candidates. Return (best_sql, full_ranking).
    """
    # Deduplicate
    seen = set()
    unique = []
    for sql in candidates:
        normalized = re.sub(r"\\s+", " ", sql.strip().lower())
        if normalized not in seen:
            seen.add(normalized)
            unique.append(sql)

    scored = [score_sql(sql, intent_keywords) for sql in unique]
    scored.sort(key=lambda x: x["score"], reverse=True)

    best = scored[0]["sql"] if scored[0]["valid"] else None
    return best, scored
