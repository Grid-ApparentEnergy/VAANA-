"""
Safe PostgreSQL execution.
- Read-only (rag_user has SELECT only anyway)
- Row limit enforced
- Timeout enforced
- Event code translation applied post-execution
"""
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from config.settings import settings
from core.event_translator import translate_event_codes_in_df

class ExecutionResult:
    def __init__(
        self,
        df: pd.DataFrame | None = None,
        error: str | None = None,
        row_count: int = 0,
        truncated: bool = False,
    ):
        self.df = df
        self.error = error
        self.row_count = row_count
        self.truncated = truncated
        self.success = error is None

def get_engine():
    url = (
        f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
        f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    )
    # Try psycopg2 first, fall back to pg8000 if not available
    try:
        return create_engine(url, connect_args={"connect_timeout": 10})
    except Exception:
        url_pg8000 = url.replace("psycopg2", "pg8000")
        return create_engine(url_pg8000)

def execute_sql(sql: str) -> ExecutionResult:
    """
    Execute SQL safely. Returns ExecutionResult with DataFrame.
    Applies row limit and event code translation.
    """
    
    # Inject LIMIT if not present
    sql_stripped = sql.strip().rstrip(";")
    sql_lower = sql_stripped.lower()
    if "limit " not in sql_lower:
        sql_with_limit = f"SELECT * FROM ({sql_stripped}) AS _q LIMIT {settings.max_rows + 1}"
    else:
        sql_with_limit = sql_stripped

    engine = get_engine()
    try:
        with engine.connect() as conn:
            conn.execute(text(f"SET statement_timeout = '{settings.query_timeout_seconds * 1000}'"))
            df = pd.read_sql(text(sql_with_limit), conn)

        truncated = len(df) > settings.max_rows
        df = df.head(settings.max_rows)

        # Translate event codes in any column named 'event_code'
        df = translate_event_codes_in_df(df)

        return ExecutionResult(
            df=df,
            row_count=len(df),
            truncated=truncated,
        )

    except Exception as e:
        if "timeout" in str(e).lower():
            return ExecutionResult(
                error=f"Query exceeded {settings.query_timeout_seconds}s timeout. "
                      "Try narrowing the time range or adding more filters."
            )
        return ExecutionResult(error=f"Database error: {str(e)}")
    except psycopg2.Error as e:
        return ExecutionResult(error=f"Database error: {str(e)}")
    except Exception as e:
        return ExecutionResult(error=f"Unexpected error: {str(e)}")
