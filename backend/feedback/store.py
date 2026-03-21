"""
Stores user feedback on query results.
Schema:
  id | query | sql_used | rating | comment | timestamp | retrain_used
"""
import sqlite3
import datetime
from config.settings import settings

def init_db():
    conn = sqlite3.connect(settings.feedback_db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            query       TEXT NOT NULL,
            sql_used    TEXT NOT NULL,
            rating      INTEGER NOT NULL,   -- 1 (thumbs up) or -1 (thumbs down)
            comment     TEXT,
            timestamp   TEXT NOT NULL,
            retrain_used INTEGER DEFAULT 0  -- 1 once used for Vanna retraining
        )
    """)
    conn.commit()
    conn.close()

def save_feedback(query: str, sql_used: str, rating: int, comment: str = "") -> int:
    init_db() # ensure db exists
    conn = sqlite3.connect(settings.feedback_db_path)
    cur = conn.execute(
        "INSERT INTO feedback (query, sql_used, rating, comment, timestamp) VALUES (?,?,?,?,?)",
        (query, sql_used, rating, comment, datetime.datetime.utcnow().isoformat())
    )
    feedback_id = cur.lastrowid
    conn.commit()
    conn.close()
    return feedback_id

def get_positive_feedback(limit: int = 50) -> list[dict]:
    """Get thumbs-up feedback not yet used for retraining."""
    init_db()
    conn = sqlite3.connect(settings.feedback_db_path)
    rows = conn.execute(
        "SELECT id, query, sql_used FROM feedback WHERE rating = 1 AND retrain_used = 0 LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [{"id": r[0], "query": r[1], "sql": r[2]} for r in rows]

def mark_retrained(feedback_ids: list[int]):
    conn = sqlite3.connect(settings.feedback_db_path)
    conn.executemany(
        "UPDATE feedback SET retrain_used = 1 WHERE id = ?",
        [(fid,) for fid in feedback_ids]
    )
    conn.commit()
    conn.close()
