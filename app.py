import asyncio
import logging
import os
from typing import Any

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp.types import CallToolRequestParams, CallToolResult

from mcp_use import MCPAgent, MCPClient
from mcp_use.client.config import load_config_file
from mcp_use.client.middleware import Middleware, MiddlewareContext


class StripNoneToolArgumentsMiddleware(Middleware):
    """Playwright MCP rejects JSON null for optional string fields; strip nulls before tools/call."""

    async def on_call_tool(
        self,
        context: MiddlewareContext[CallToolRequestParams],
        call_next: Any,
    ) -> CallToolResult:
        args = context.params.arguments
        if args:
            cleaned = {k: v for k, v in args.items() if v is not None}
            if cleaned != args:
                context.params.arguments = cleaned
        return await call_next(context)


BROWSER_AGENT_INSTRUCTIONS = (
    "When using Playwright browser tools: only call tools that appear in the tool list. "
    "There is no browser_open_file tool. Open URLs with browser_navigate, interact with "
    "browser_click / browser_type / browser_press_key, then use browser_snapshot. "
    "For optional parameters (e.g. browser_snapshot filename), omit the field entirely—"
    "never pass null.\n\n"
    "Web search (Google, Bing, etc.): do NOT type into the google.com homepage search bar "
    "unless the snapshot clearly shows a ref on the real query field (input/textarea/searchbox). "
    "Google's UI often maps refs to outer divs that cannot be filled. The reliable approach is "
    "browser_navigate to a search-results URL with an encoded query, e.g. "
    "https://www.google.com/search?q=bollywood (replace bollywood with the user's terms; "
    "encode spaces as + or %20, and encode other special characters). "
    "After that, use browser_snapshot to confirm results."
)

async def run_memory_chat():

    load_dotenv()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    # Avoid noisy Unicode logging issues on Windows terminals.
    logging.getLogger("mcp_use").setLevel(logging.WARNING)

    # To get the configuration for mcp servers
    config_file = "browser_mcp.json"

    print("Initializing MCP servers...")

    client = MCPClient(
        config=load_config_file(config_file),
        middleware=[StripNoneToolArgumentsMiddleware()],
    )
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        max_tokens=1000,
        temperature=0,
    )

    # Create MCP agent with memory enabled
    agent = MCPAgent(
        client=client,
        llm=llm,
        memory_enabled=True,
        max_steps=15,
        additional_instructions=BROWSER_AGENT_INSTRUCTIONS,
    )


    print("MCP agents initialized. Starting chat...")

    try:
        # Main chat loop
        while True:

            # Read input and handle piped/closed stdin gracefully.
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print("\nInput stream closed. Exiting chat...")
                break
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Exiting chat...")
                break

            # Check for clear history command
            if user_input.lower() in ["clear", "clear history", "reset"]:
                agent.clear_conversation_history()
                print("Conversation history cleared.")

            # Generate response
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"Error: {e}")
    finally:
        # Clean up resources
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
    
