import sys, os, asyncio, json, traceback, re, pandas as pd
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'core')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vanna_setup import setup_vanna_agent
from vanna.core.user import RequestContext

QUESTIONS = [
    "How many records are in the product table to see available device types?",
    "Show me a count of records in the event_raw table for the last 7 days.",
    "What are the active business services for device dev__EEOT4056946?",
    "Which cities have the most service points? List top 5.",
    "Show me the first 5 records from the device table."
]

def find_sql_recursive(d):
    """Recursively search for SQL in a nested dictionary/list."""
    if isinstance(d, dict):
        # Prefer 'sql' or 'code' keys that contain SELECT
        for k, v in d.items():
            if k in ["sql", "code"] and isinstance(v, str) and "SELECT" in v.upper():
                return v
        # Otherwise keep searching
        for v in d.values():
            res = find_sql_recursive(v)
            if res: return res
    elif isinstance(d, list):
        for item in d:
            res = find_sql_recursive(item)
            if res: return res
    return None

async def run_batch():
    print("Initializing Vanna agent...")
    agent = setup_vanna_agent()
    
    results = []
    
    for i, q in enumerate(QUESTIONS):
        print(f"\n--- Running Query {i+1}/{len(QUESTIONS)} ---")
        print(f"Question: {q}")
        
        ctx = RequestContext(metadata={"source": "batch_test"}, remote_addr="127.0.0.1")
        
        raw_chunks = []
        final_sql = ""
        
        async for component in agent.send_message(
            request_context=ctx,
            message=q,
            conversation_id=f"batch-test-{datetime.now().strftime('%H%M%S')}"
        ):
            # 1. Capture SQL using model_dump
            try:
                comp_data = component.model_dump()
                sql_found = find_sql_recursive(comp_data)
                if sql_found:
                    final_sql = sql_found.strip()
            except:
                pass

            # 2. Capture Text (Raw for now)
            text_chunk = ""
            if hasattr(component, "content") and component.content:
                text_chunk = component.content
            elif hasattr(component, "simple_component") and hasattr(component.simple_component, "text"):
                text_chunk = component.simple_component.text
            elif hasattr(component, "rich_component"):
                rc = component.rich_component
                if hasattr(rc, "description"): text_chunk = rc.description
                elif hasattr(rc, "text"): text_chunk = rc.text
            
            if text_chunk:
                raw_chunks.append(text_chunk)

        # 3. Clean and filter the response
        # We want to ignore any noise (tool logs) and standard table listings
        noise_patterns = [
            r"Tool failed", r"Tool completed", r"Results saved to file", 
            r"IMPORTANT: FOR VISUALIZE_DATA", r"Error executing query", 
            r"relation \".*\" does not exist", r"column \".*\" does not exist",
            r"Perhaps you meant to reference", r"LINE \d+:", r"\^",
            r"table_name.*interval_raw", r"column_name.*insert_ts"
        ]
        
        clean_response = ""
        for chunk in raw_chunks:
            if not any(re.search(p, chunk, re.IGNORECASE | re.DOTALL) for p in noise_patterns):
                clean_response += chunk + " "
        
        # Final cleanup of common artifacts
        clean_response = re.sub(r'\s+', ' ', clean_response).strip()
        # Remove empty bracketed downloads or paths if any
        clean_response = re.sub(r'\[Download the .* records\]\(sandbox:/mnt/data/.*\.csv\)', '', clean_response)
        
        if not final_sql:
            # Last ditch: check if it's in a markdown block in the raw chunks
            for chunk in raw_chunks:
                match = re.search(r"```sql\n(.*?)\n```", chunk, re.IGNORECASE | re.DOTALL)
                if match:
                    final_sql = match.group(1).strip()
                    break

        print(f"Final SQL Captured: {final_sql[:80]}...")
        
        results.append({
            "question": q,
            "sql": final_sql if final_sql else "SQL NOT FOUND",
            "response": clean_response
        })

        # Terminal Table Preview for Batch Test
        # Search in raw_chunks instead of clean_response to avoid filtered out filenames
        all_raw_text = " ".join(raw_chunks)
        csv_matches = re.findall(r'query_results_[a-f0-9]+\.csv', all_raw_text)
        if csv_matches:
            for csv_file in set(csv_matches):
                if os.path.exists(csv_file):
                    print(f"\n[Preview Results from {csv_file}]:")
                    try:
                        df = pd.read_csv(csv_file)
                        if not df.empty:
                            print(df.head(5).to_string(index=False))
                        else:
                            print("(Empty table)")
                    except:
                        pass

    # Save to JSON
    output_file = "new_training_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[OK] Batch queries complete. Results saved to {output_file}")

if __name__ == "__main__":
    try:
        asyncio.run(run_batch())
    except Exception as e:
        print(f"[ERROR] Batch run failed: {e}")
        traceback.print_exc()
