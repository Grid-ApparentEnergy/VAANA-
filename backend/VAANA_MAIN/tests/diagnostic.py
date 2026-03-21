import os, sys, asyncio
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from vanna_setup import setup_vanna_agent
from vanna.core.user import RequestContext

async def run_diagnostic():
    print("--- Vanna Diagnostic Start ---")
    agent = setup_vanna_agent()
    
    ctx = RequestContext(metadata={"source": "diagnostic"}, remote_addr="127.0.0.1")
    question = "How many records are in the product table?"
    
    print(f"Question: {question}")
    print("Thinking...")
    
    full_response = ""
    async for component in agent.send_message(
        request_context=ctx,
        message=question,
        conversation_id="diag-123"
    ):
        print(f"[Debug] Received component: {type(component)}")
        if hasattr(component, "content") and component.content:
            full_response += component.content
        elif hasattr(component, "simple_component") and hasattr(component.simple_component, "text"):
            full_response += component.simple_component.text
        elif hasattr(component, "rich_component"):
            rc = component.rich_component
            if hasattr(rc, "description"): full_response += f" {rc.description}"
            elif hasattr(rc, "text"): full_response += f" {rc.text}"
            
            # Check for SQL in rich component
            if hasattr(rc, "sql"): print(f"[Debug] SQL Found: {rc.sql}")
            elif hasattr(rc, "code"): print(f"[Debug] Code Found: {rc.code}")

    if not full_response:
        print("[Warn] No text response captured.")
    
    print("\n--- Response ---")
    print(full_response)
    print("--- Vanna Diagnostic End ---")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
