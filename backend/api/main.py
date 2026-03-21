from fastapi import FastAPI
from api.routers import query, feedback, streaming

app = FastAPI(
    title="MDM Vanna AI Wrapper",
    description="LLM-integrated backend for Meter Data Management querying.",
    version="1.0.0"
)

app.include_router(query.router)
app.include_router(feedback.router)
app.include_router(streaming.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/debug/test-sql")
def test_sql_generation():
    """Debug endpoint to test SQL generation directly"""
    from core import vanna_direct
    
    question = "Show me devices by type"
    try:
        sql = vanna_direct.generate_sql(question)
        return {
            "question": question,
            "sql": sql,
            "success": sql is not None
        }
    except Exception as e:
        return {
            "question": question,
            "error": str(e),
            "success": False
        }
