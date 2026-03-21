import sys, os, asyncio, traceback
sys.path.insert(0, '.')

print("Step 1: Importing config...")
from config import CHROMA_DB_PATH, POSTGRES_DB_CONFIG, OPENAI_API_KEY
print(f"  OPENAI_API_KEY set: {bool(OPENAI_API_KEY)}")
print(f"  Postgres host: {POSTGRES_DB_CONFIG['host']}")
print(f"  ChromaDB path: {CHROMA_DB_PATH}")
print(f"  ChromaDB exists: {os.path.exists(CHROMA_DB_PATH)}")

print("\nStep 2: Testing Postgres connectivity...")
try:
    import psycopg2
    conn = psycopg2.connect(**POSTGRES_DB_CONFIG, connect_timeout=10)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
    count = cur.fetchone()[0]
    print(f"  [OK] Connected! Public tables: {count}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"  [ERROR] Postgres connection failed: {e}")

print("\nStep 3: Initializing Vanna agent...")
try:
    from vanna_setup import setup_vanna_agent
    agent = setup_vanna_agent()
    print("  [OK] Agent created successfully.")
except Exception as e:
    print(f"  [ERROR] Agent setup failed: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\nStep 4: Checking training status...")
try:
    # Access collection through agent memory to avoid config conflicts
    coll = agent.agent_memory._get_collection()
    doc_count = coll.count()
    print(f"  [OK] ChromaDB collection has {doc_count} documents.")
    
    if doc_count == 0:
        print("\n[Info] ChromaDB is empty. Running training...")
        from training import train_agent
        train_agent(agent)
        print("[OK] Training complete.")
    else:
        print(f"  [OK] Skipping training — {doc_count} docs already in ChromaDB.")
except Exception as e:
    print(f"  [ERROR] Error during training check: {e}")
    traceback.print_exc()


print("\nStep 5: Sending a live query to the agent...")
async def test_query(agent):
    from vanna.core.user import RequestContext
    ctx = RequestContext(metadata={"source": "test"}, remote_addr="127.0.0.1")
    full_response = ""
    async for component in agent.send_message(
        request_context=ctx,
        message="How many records are in the public.device table?",
        conversation_id="test-session"
    ):
        if hasattr(component, "content") and component.content:
            full_response += component.content
        elif hasattr(component, "simple_component") and hasattr(component.simple_component, "text"):
            full_response += component.simple_component.text
        elif hasattr(component, "rich_component"):
            rc = component.rich_component
            if hasattr(rc, "description"):
                full_response += f"\n{rc.description}"
            elif hasattr(rc, "text"):
                full_response += rc.text

    if full_response:
        print("\n--- Response ---")
        print(full_response[:3000])
        print("----------------")
    else:
        print("[WARN] No text response received from the agent.")

try:
    asyncio.run(test_query(agent))
except Exception as e:
    print(f"[ERROR] Query failed: {e}")
    traceback.print_exc()

print("\nDone.")
