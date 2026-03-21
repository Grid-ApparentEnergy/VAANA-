import os
import sys

# Ensure the core directory is in the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from config import CHROMA_DB_PATH, CHROMA_COLLECTION_NAME
from vanna_setup import setup_vanna_agent
from training import train_agent
from vanna_cli import run_cli, run_cli_sync

def main():
    print("=== Vanna AI Terminal Setup ===")
    
    # Initialize the agent
    agent = setup_vanna_agent()
    
    # Check if collection has been trained (folder alone is not enough — ChromaDB creates it on init)
    import chromadb as _chromadb
    _client = _chromadb.PersistentClient(path=CHROMA_DB_PATH)
    _coll = _client.get_or_create_collection(CHROMA_COLLECTION_NAME)
    _doc_count = _coll.count()

    if _doc_count > 0:
        print(f"\n[OK] Found existing ChromaDB memory ({_doc_count} docs). Skipping training.")
        print("   (To retrain, delete the ChromaDB folder and restart).")
    else:
        print(f"\n[Info] ChromaDB is empty. Starting training...")
        train_agent(agent)
    
    # Run the interactive CLI
    from vanna_cli import run_cli
    from vanna_cli import run_cli_sync
    run_cli_sync(agent)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting Vanna CLI. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Error] Critical Error: {e}")
        sys.exit(1)