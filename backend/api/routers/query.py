from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.vanna_client import generate_sql, train_if_needed
from core.prompt_multiplier import extract_entities, generate_prompt_variations
from core.sql_comparator import rank_sql_candidates
from core.executor import execute_sql
from core.response_structurer import structure_response
from guardrails.input_guard import check_input
from guardrails.output_guard import sanitize_response
import time

router = APIRouter(prefix="/query", tags=["query"])

class QueryRequest(BaseModel):
    query: str
    device_id: str = ""
    period_type: str = "THIS_WEEK"

class QueryResponse(BaseModel):
    status: str
    summary: str
    insights: list = []
    kpis: list
    charts: list
    tables: list
    metadata: dict
    sql_used: str = ""
    debug: dict = {}   # Only populated in dev mode

@router.post("/", response_model=QueryResponse)
async def run_query(req: QueryRequest):
    start_time = time.time()
    
    # 0. Ensure Vanna is trained
    train_if_needed()

    # 1. Input guardrail
    guard = check_input(req.query)
    if not guard.allowed:
        raise HTTPException(status_code=400, detail=guard.reason)

    # 2. Extract entities + generate 5 prompt variations
    entities = extract_entities(req.query)
    if req.device_id:
        entities["device_ids"] = [req.device_id]
    variations = generate_prompt_variations(req.query, entities)

    # 3. Generate SQL for each variation via Vanna
    sql_candidates = []
    for i, prompt in enumerate(variations):
        try:
            sql = await generate_sql(prompt)
            if sql:
                sql_candidates.append(sql)
        except Exception:
            pass

    if not sql_candidates:
        raise HTTPException(status_code=422, detail="Could not generate SQL for this query.")

    # 4. Rank candidates, pick best
    intent_keywords = entities.get("metric_types", [])
    best_sql, ranking = rank_sql_candidates(sql_candidates, intent_keywords)

    if not best_sql:
        raise HTTPException(status_code=422, detail="No valid SQL could be generated.")

    # 5. Execute
    result = execute_sql(best_sql)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    # 6. Structure response with AI orchestration
    execution_time_ms = int((time.time() - start_time) * 1000)
    structured = structure_response(
        df=result.df,
        user_query=req.query,
        device_id=req.device_id or entities.get("device_ids", ["unknown"])[0] if entities.get("device_ids") else "unknown",
        period_type=req.period_type,
        row_count=result.row_count,
        truncated=result.truncated,
        sql_used=best_sql,
    )
    
    # Add debug metadata
    structured["debug"] = {
        "sql": best_sql,
        "execution_time_ms": execution_time_ms,
        "ranking": ranking
    }

    # 7. Sanitize (strip model names, internals)
    clean = sanitize_response(structured)

    return QueryResponse(**clean, sql_used=best_sql)
