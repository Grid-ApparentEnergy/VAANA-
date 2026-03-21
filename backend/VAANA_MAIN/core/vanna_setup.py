from vanna import Agent, AgentConfig
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, User, RequestContext
from vanna.integrations.openai import OpenAILlmService
from vanna.integrations.postgres import PostgresRunner
from vanna.integrations.chromadb import ChromaAgentMemory
from vanna.tools import RunSqlTool
from config import * 
import json

# Support legacy training methods in 2.0.2 ChromaAgentMemory
class TrainableChromaMemory(ChromaAgentMemory):
    """
    A wrapper for ChromaAgentMemory that adds legacy training methods (add_ddl, add_documentation, add_sql)
    for compatibility with older training scripts, while storing data in the new 2.0 format.
    """
    def add_ddl(self, ddl: str, **kwargs):
        import uuid
        print(f"[Info] Training DDL (Legacy Mode)...")
        collection = self._get_collection()
        doc_id = f"ddl-{uuid.uuid4().hex[:8]}"
        collection.upsert(
            ids=[doc_id],
            documents=[ddl],
            metadatas=[{"type": "ddl", "is_text_memory": True}]
        )
        print(f"[OK] DDL stored in ChromaDB (ID: {doc_id})")

    def add_documentation(self, documentation: str, **kwargs):
        import uuid
        print(f"[Info] Training Documentation (Legacy Mode)...")
        collection = self._get_collection()
        doc_id = f"doc-{uuid.uuid4().hex[:8]}"
        collection.upsert(
            ids=[doc_id],
            documents=[documentation],
            metadatas=[{"type": "documentation", "is_text_memory": True}]
        )
        print(f"[OK] Documentation stored in ChromaDB (ID: {doc_id})")

    def add_sql(self, question: str, sql: str, **kwargs):
        import uuid
        import json
        print(f"[Info] Training SQL Example (Legacy Mode)...")
        collection = self._get_collection()
        doc_id = f"sql-{uuid.uuid4().hex[:8]}"
        
        # Tool usage memory format
        usage_data = json.dumps({
            "question": question,
            "tool_name": "run_sql",
            "tool_args": {"sql": sql}
        })
        
        collection.upsert(
            ids=[doc_id],
            documents=[usage_data],
            metadatas=[{
                "type": "sql_example", 
                "is_tool_usage_memory": True,
                "question": question
            }]
        )
        print(f"[OK] SQL Example stored in ChromaDB (ID: {doc_id})")


class CorrectingRunSqlTool(RunSqlTool):
    """
    A wrapper for RunSqlTool that automatically corrects common SQL hallucinations,
    specifically pluralized table names like 'business_services' and 'service_points'.
    """
    async def execute(self, context, args):
        if hasattr(args, "sql") and args.sql:
            original_sql = args.sql
            # Fix known pluralization hallucinations
            corrected_sql = original_sql.replace("business_services", "business_service") \
                                        .replace("service_points", "service_point") \
                                        .replace("business_services", "business_service") \
                                        .replace("addresses", "address")
            
            if corrected_sql != original_sql:
                print(f"\n[Info] Auto-correcting SQL: \n  From: {original_sql}\n  To:   {corrected_sql}")
                args.sql = corrected_sql
        
        return await super().execute(context, args)


# User Resolver for CLI
class CLIUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="cli-user-001", 
            username="Admin", 
            email="admin@local", 
            group_memberships=["admin"] 
        )

# Initialize Components
def setup_vanna_agent():
    llm = OpenAILlmService(api_key=OPENAI_API_KEY, model="gpt-4o")
    
    memory = TrainableChromaMemory(
        persist_directory=CHROMA_DB_PATH, 
        collection_name=CHROMA_COLLECTION_NAME
    )
    
    sql_runner = PostgresRunner(**POSTGRES_DB_CONFIG)
    
    tools = ToolRegistry()
    tools.register_local_tool(
        CorrectingRunSqlTool(sql_runner=sql_runner), 
        access_groups=['admin'] 
    )
    
    agent = Agent(
        llm_service=llm,
        tool_registry=tools,
        user_resolver=CLIUserResolver(), 
        agent_memory=memory,
        config=AgentConfig()
    )
    
    return agent

