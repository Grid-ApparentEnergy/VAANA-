import re
import sqlglot
from .rules import BLOCKED_SQL_KEYWORDS, ALLOWED_TABLES
from config.settings import settings

class OutputGuardResult:
    def __init__(self, allowed: bool, reason: str = ""):
        self.allowed = allowed
        self.reason = reason

def check_sql(sql: str) -> OutputGuardResult:
    """
    Validates generated SQL before execution.
    Must be SELECT-only, only touches allowed tables,
    no system catalog access, no dangerous keywords.
    """
    sql_upper = sql.upper().strip()

    # 1. Must start with SELECT or WITH
    if not (sql_upper.startswith("SELECT") or sql_upper.startswith("WITH")):
        return OutputGuardResult(False, "Only SELECT queries are allowed.")

    # 2. Blocked SQL keywords check
    for kw in BLOCKED_SQL_KEYWORDS:
        if kw.upper() in sql_upper:
            return OutputGuardResult(False, f"Blocked keyword detected: {kw}")

    # 3. Parse with sqlglot and check table references
    try:
        parsed = sqlglot.parse_one(sql, dialect="postgres")
        tables = {
            t.name.lower()
            for t in parsed.find_all(sqlglot.exp.Table)
            if t.name
        }
        disallowed = tables - ALLOWED_TABLES
        if disallowed:
            return OutputGuardResult(
                False, f"Query references disallowed tables: {disallowed}"
            )
    except Exception:
        # If parsing fails, do keyword-based fallback only
        pass

    # 4. No DDL/DML allowed
    if not settings.allow_ddl_queries:
        ddl_patterns = ["CREATE", "DROP", "ALTER", "TRUNCATE"]
        for p in ddl_patterns:
            if p in sql_upper:
                return OutputGuardResult(False, "DDL statements not allowed.")

    return OutputGuardResult(True)

def sanitize_response(response: dict) -> dict:
    """
    Remove any internal metadata from response before sending to user.
    Never expose: model name, SQL internals, schema details, API keys.
    """
    KEYS_TO_STRIP = ["model", "sql_candidates", "vanna_config", "db_config", "raw_sql"]
    if not settings.model_name_disclosure:
        KEYS_TO_STRIP += ["openai_model", "llm_model", "ai_model"]

    return {k: v for k, v in response.items() if k not in KEYS_TO_STRIP}
