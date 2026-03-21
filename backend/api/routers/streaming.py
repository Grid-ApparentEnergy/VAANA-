"""
Streaming router for real-time agent state updates.
Integrates with the existing Vanna AI pipeline.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
from core.vanna_client import train_if_needed
from core.prompt_multiplier import extract_entities, generate_prompt_variations
from core.sql_comparator import rank_sql_candidates
from core.executor import execute_sql
from core.response_structurer import structure_response
from guardrails.input_guard import check_input
from guardrails.output_guard import sanitize_response

router = APIRouter(prefix="/stream", tags=["streaming"])

class StreamQueryRequest(BaseModel):
    query: str
    device_id: str = ""
    period_type: str = "THIS_WEEK"

async def stream_query_response(query: str, device_id: str = "", period_type: str = "THIS_WEEK"):
    """
    Stream the query processing pipeline with real-time state updates.
    
    States:
    1. thinking - Initial analysis and validation
    2. generating_query - Creating SQL variations
    3. fetching_data - Executing SQL and retrieving data
    4. composing_response - Structuring the final response
    """
    
    try:
        # State 1: Thinking - Input validation
        yield json.dumps({
            "type": "state",
            "state": "thinking",
            "message": "Analyzing your question..."
        }) + "\n"
        await asyncio.sleep(0.3)
        
        # Ensure Vanna is trained
        train_if_needed()
        
        # Input guardrail check
        guard = check_input(query)
        if not guard.allowed:
            yield json.dumps({
                "type": "error",
                "message": f"Input validation failed: {guard.reason}"
            }) + "\n"
            return
        
        # State 2: Generating Query - Extract entities and create SQL
        yield json.dumps({
            "type": "state",
            "state": "generating_query",
            "message": "Generating SQL queries..."
        }) + "\n"
        await asyncio.sleep(0.3)
        
        # Extract entities
        entities = extract_entities(query)
        if device_id:
            entities["device_ids"] = [device_id]
        
        # Generate prompt variations
        variations = generate_prompt_variations(query, entities)
        
        yield json.dumps({
            "type": "progress",
            "message": f"Generated {len(variations)} query variations"
        }) + "\n"
        await asyncio.sleep(0.2)
        
        # Generate SQL candidates
        from core.vanna_client import generate_sql
        sql_candidates = []
        for i, prompt in enumerate(variations):
            try:
                sql = await generate_sql(prompt)
                if sql:
                    sql_candidates.append(sql)
                    yield json.dumps({
                        "type": "progress",
                        "message": f"Generated SQL candidate {i+1}/{len(variations)}"
                    }) + "\n"
                    await asyncio.sleep(0.1)
            except Exception as e:
                yield json.dumps({
                    "type": "progress",
                    "message": f"Skipped variation {i+1} (generation failed)"
                }) + "\n"
        
        if not sql_candidates:
            yield json.dumps({
                "type": "error",
                "message": "Could not generate valid SQL for this query"
            }) + "\n"
            return
        
        # Rank and select best SQL
        intent_keywords = entities.get("metric_types", [])
        best_sql, ranking = rank_sql_candidates(sql_candidates, intent_keywords)
        
        if not best_sql:
            yield json.dumps({
                "type": "error",
                "message": "No valid SQL could be selected"
            }) + "\n"
            return
        
        # State 3: Fetching Data - Execute SQL
        yield json.dumps({
            "type": "state",
            "state": "fetching_data",
            "message": "Retrieving data from database..."
        }) + "\n"
        await asyncio.sleep(0.3)
        
        # Execute the SQL
        result = execute_sql(best_sql)
        
        if not result.success:
            yield json.dumps({
                "type": "error",
                "message": f"Query execution failed: {result.error}"
            }) + "\n"
            return
        
        yield json.dumps({
            "type": "progress",
            "message": f"Retrieved {result.row_count} rows"
        }) + "\n"
        await asyncio.sleep(0.2)
        
        # State 4: Composing Response - Structure the output
        yield json.dumps({
            "type": "state",
            "state": "composing_response",
            "message": "Structuring your answer..."
        }) + "\n"
        await asyncio.sleep(0.3)
        
        # Structure the response
        device_id_final = device_id or (entities.get("device_ids", ["unknown"])[0] if entities.get("device_ids") else "unknown")
        structured = structure_response(
            df=result.df,
            user_query=query,
            device_id=device_id_final,
            period_type=period_type,
            row_count=result.row_count,
            truncated=result.truncated,
        )
        
        # Sanitize response
        clean = sanitize_response(structured)
        
        # Final response with complete data
        yield json.dumps({
            "type": "response",
            "data": clean,
            "sql_used": best_sql,
            "metadata": {
                "query": query,
                "row_count": result.row_count,
                "truncated": result.truncated,
                "sql_candidates_count": len(sql_candidates)
            }
        }) + "\n"
        
    except Exception as e:
        yield json.dumps({
            "type": "error",
            "message": f"Unexpected error: {str(e)}"
        }) + "\n"

@router.post("/query")
async def stream_query(request: StreamQueryRequest):
    """
    Stream query processing with real-time state updates.
    Returns newline-delimited JSON (NDJSON) stream.
    """
    return StreamingResponse(
        stream_query_response(
            query=request.query,
            device_id=request.device_id,
            period_type=request.period_type
        ),
        media_type="application/x-ndjson"
    )

@router.get("/health")
async def stream_health():
    """Health check for streaming endpoint"""
    return {"status": "ok", "message": "Streaming endpoint is ready"}
