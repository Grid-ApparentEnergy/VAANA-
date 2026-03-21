"""
VANNA BRIDGE — Single integration point for the VAANA_MAIN Vanna AI module.
All imports from VAANA_MAIN happen here. Nothing else imports VAANA_MAIN directly.
"""

import os
import sys

# The backend/config package inevitably shadows VAANA_MAIN/core/config.py.
# To let vanna_setup load the correct variables (like OPENAI_API_KEY), we momentarily pop it.
_vaana_main_core_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../VAANA_MAIN/core'))

_old_config = sys.modules.pop('config', None)
sys.path.insert(0, _vaana_main_core_path)

try:
    from vanna_setup import setup_vanna_agent
    from training import train_agent as _train_agent
finally:
    # Cleanup and restore Original configurations layout universally
    sys.path.pop(0)
    sys.modules.pop('config', None)
    if _old_config is not None:
        sys.modules['config'] = _old_config

from config.settings import settings
from config.ddl import MDM_DDL
from config.documentation import MDM_DOCUMENTATION
from config.event_codes import ALLOWED_EVENTS, EVENT_PAIRS

# ── Singleton ────────────────────────────────────────────────
_vanna_instance = None

def get_vanna():
    """
    Returns the singleton Vanna instance initialized by VAANA_MAIN.
    """
    global _vanna_instance
    if _vanna_instance is not None:
        return _vanna_instance

    _vanna_instance = setup_vanna_agent()
    return _vanna_instance

# ── Training ─────────────────────────────────────────────────
TRAINED_FLAG = os.path.join(os.path.dirname(__file__), "../vanna_2_0_chroma_db/.trained")

def train_if_needed(force: bool = False) -> dict:
    """
    Trains Vanna on DDL + documentation + event codes + example Q&A pairs.
    Idempotent — skips if already trained unless force=True.
    """
    if not force and os.path.exists(TRAINED_FLAG):
        return {"trained": False, "reason": "already_trained"}

    try:
        vn = get_vanna()
        
        # 1. DDL — Reading from the explicit data directory provided by the user
        mdm_ddl_path = os.path.join(os.path.dirname(__file__), '../VAANA_MAIN/data/mdm-ddl.sql')
        with open(mdm_ddl_path, 'r', encoding='utf-8') as f:
            full_ddl = f.read()
        vn.agent_memory.add_ddl(full_ddl)

        # 2. Domain documentation
        vn.agent_memory.add_documentation(MDM_DOCUMENTATION)

        # 3. Event codes — teach Vanna what each code means
        event_lines = ["Event codes in event_raw table (event_code column stores these as strings like '0101'):"]
        for e in ALLOWED_EVENTS:
            event_lines.append(
                f"  Code {str(e['id']).zfill(4)}: {e['description']} | "
                f"Severity: {e['severity']} | Category: {e['category']}"
            )
        event_lines.append("\nOccurrence -> Restoration pairs:")
        for occ, rst in EVENT_PAIRS:
            event_lines.append(f"  {str(occ).zfill(4)} -> {str(rst).zfill(4)}")
        
        vn.agent_memory.add_documentation("\n".join(event_lines))

        # 4. Seed known-good example Q&A pairs
        _seed_examples(vn)

        os.makedirs(os.path.dirname(TRAINED_FLAG), exist_ok=True)
        open(TRAINED_FLAG, "w").close()
        return {"trained": True, "reason": "completed"}
    except Exception as e:
        print(f"[vanna_bridge] Training error: {e}")
        return {"trained": False, "reason": str(e)}

def _seed_examples(vn) -> None:
    import json
    import os
    examples_path = os.path.join(os.path.dirname(__file__), '../VAANA_MAIN/data/examples.json')
    if os.path.exists(examples_path):
        try:
            with open(examples_path, 'r', encoding='utf-8') as f:
                examples = json.load(f)
            for item in examples:
                if "question" in item and "sql" in item:
                    vn.agent_memory.add_sql(question=item["question"], sql=item["sql"])
            print("[vanna_bridge] Explicit examples.json seeded successfully.")
        except Exception as e:
            print(f"[vanna_bridge] Failed to seed examples.json: {e}")
    else:
        print("[vanna_bridge] WARNING: examples.json not found in data directory.")

# ── SQL Generation ────────────────────────────────────────────
async def generate_sql(prompt: str) -> str | None:
    """Generate SQL from a natural language prompt using OpenAI natively with Vanna Chroma Memory."""
    try:
        import os
        import chromadb
        from openai import AsyncOpenAI
        from config.settings import settings
        
        # Direct fallback for standard installations
        vn = get_vanna()
        if hasattr(vn, 'generate_sql'):
            return vn.generate_sql(question=prompt)
            
        # Connect directly to the underlying Chroma vector index
        chroma_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../vanna_2_0_chroma_db'))
        client = chromadb.PersistentClient(path=chroma_path)
        coll = client.get_collection('mdm_memory_v2')
        
        # Retrieve the closest context logic securely matching Vanna 2.x chunks
        results = coll.query(query_texts=[prompt], n_results=10)
        context_docs = results['documents'][0] if results and results['documents'] else []
        
        # Construct explicit unyielding instructions
        system_msg = (
            "You are a PostgreSQL expert. Based on the provided database schema and documentation, "
            "generate ONLY a valid, raw SQL query to answer the user's question. Do not include "
            "explanations, conversational text, markdown formatting, or ```sql blocks. Output the raw query exclusively."
        )
        if context_docs:
            system_msg += "\n\nDatabase Context:\n" + "\n---\n".join(context_docs)
            
        # Run asynchronously maintaining the FastAPI Uvicorn threads optimally
        oai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        completion = await oai_client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        sql = completion.choices[0].message.content.strip()
        
        # Sanitize common markdown artifacts defensively
        if sql.lower().startswith("```sql"): sql = sql[6:]
        if sql.startswith("```"): sql = sql[3:]
        if sql.endswith("```"): sql = sql[:-3]
        
        return sql.strip()
        
    except Exception as e:
        print(f"[vanna_bridge] generate_sql error: {e}")
        return None

# ── SQL Execution (via Vanna's built-in runner if available) ──
def run_sql_via_vanna(sql: str):
    """
    Optional: Use Vanna's built-in SQL runner if it exists.
    Falls back to core/executor.py otherwise.
    """
    vn = get_vanna()
    if hasattr(vn, "run_sql"):
        return vn.run_sql(sql)
    return None
