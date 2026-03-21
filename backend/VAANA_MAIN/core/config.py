import os
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# PostgreSQL Configuration
POSTGRES_DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'port': os.getenv("DB_PORT")
}

# ChromaDB Configuration
CHROMA_DB_PATH = "./vanna_2_0_chroma_db"
CHROMA_COLLECTION_NAME = "mdm_memory_v2"
