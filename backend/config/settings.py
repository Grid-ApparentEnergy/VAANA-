from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o"

    db_host: str
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    max_rows: int = 5000
    query_timeout_seconds: int = 60
    
    # Optional legacy fields (not used in vanna_direct)
    chroma_db_path: str = "./vanna_2_0_chroma_db"
    chroma_collection_name: str = "mdm_memory_v2"
    vanna_version: str = "2.0"
    pinecone_api_key: str = ""
    pinecone_env: str = ""
    pinecone_index_name: str = "vanna"
    feedback_db_path: str = "./feedback.db"

    model_name_disclosure: bool = False
    allow_ddl_queries: bool = False
    allow_dml_queries: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env

settings = Settings()
