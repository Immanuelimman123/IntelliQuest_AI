
import asyncio

from backend.mcp_server.server import mcp


async def main():

    print("\n========== INTELLIQUEST MCP TOOL TEST ==========")

    print("\n[1] Testing search_documents")

    search_result = await mcp.call_tool(
        "search_documents",
        {
            "question": "What is a list in Python?",
            "top_k": 3
        }
    )

    print("\nSearch Result:")
    print(search_result)

    print("\n[2] Testing ask_intelliquest")

    answer_result = await mcp.call_tool(
        "ask_intelliquest",
        {
            "question": "What is a list in Python?"
        }
    )

    print("\nAI Answer:")
    print(answer_result)

    print("\n========== MCP TEST COMPLETED ==========")


if __name__ == "__main__":
    asyncio.run(main())
