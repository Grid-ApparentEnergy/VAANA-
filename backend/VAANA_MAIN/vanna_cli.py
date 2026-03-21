import sys
import asyncio
import traceback
import re
import pandas as pd
import glob
import os

async def run_cli(agent):
    print("====================================================")
    print("[Info] Vanna 2.0 CLI is ready!")
    print("Type your question below. Type 'exit' or 'quit' to stop.")
    print("====================================================\n")
    
    while True:
        try:
            # Get input in a way that works with the async event loop
            loop = asyncio.get_event_loop()
            user_input = await loop.run_in_executor(None, input, "\n> Ask a question: ")
            user_input = user_input.strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("Exiting Vanna CLI. Goodbye!")
                break
            
            if not user_input:
                continue

            print("\nThinking...")
            
            # In Vanna 2.0.2, send_message requires a RequestContext
            from vanna.core.user import RequestContext
            
            # Create a basic request context for the CLI session
            request_context = RequestContext(
                metadata={"source": "cli"},
                remote_addr="127.0.0.1"
            )

            full_response = ""
            # The agent.send_message is an async generator that yields UiComponent objects
            async for component in agent.send_message(
                request_context=request_context,
                message=user_input,
                conversation_id="cli-session"
            ):
                # Extract text from either rich or simple components
                if hasattr(component, "content") and component.content:
                    full_response += component.content
                elif hasattr(component, "simple_component") and hasattr(component.simple_component, "text"):
                    # Check for SimpleTextComponent
                    full_response += component.simple_component.text
                elif hasattr(component, "rich_component"):
                    # Some rich components might have a 'description' or 'text'
                    rc = component.rich_component
                    if hasattr(rc, "description"):
                        full_response += f"\n{rc.description}"
                    elif hasattr(rc, "text"):
                        full_response += rc.text
                
                # Proactively check for data in the component
                try:
                    comp_dict = component.model_dump()
                    # If there's a chart or table, Vanna often includes a path or the data itself
                    # We'll look for CSV files in the current directory as a fallback
                except:
                    pass
            
            if full_response:
                print("\n--- Response ---")
                print(full_response)
                
                # Terminal Table Display Logic
                # Search for CSV filenames in the response text
                csv_matches = re.findall(r'query_results_[a-f0-9]+\.csv', full_response)
                if csv_matches:
                    for csv_file in set(csv_matches):
                        if os.path.exists(csv_file):
                            print(f"\n[Table Results from {csv_file}]:")
                            try:
                                df = pd.read_csv(csv_file)
                                # Display up to 10 rows
                                if not df.empty:
                                    print(df.head(10).to_string(index=False))
                                    if len(df) > 10:
                                        print(f"... and {len(df) - 10} more rows.")
                                else:
                                    print("(Empty table)")
                            except Exception as e:
                                print(f"(Could not read {csv_file}: {e})")
                
                print("----------------")
            else:
                print("\n[Warn] No text response received from the agent.")
            
        except KeyboardInterrupt:
            print("\nExiting Vanna CLI. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n[Error] Error processing request: {e}")
            traceback.print_exc()

def run_cli_sync(agent):
    """Bridge to run the async CLI from synchronous main."""
    try:
        asyncio.run(run_cli(agent))
    except KeyboardInterrupt:
        pass
