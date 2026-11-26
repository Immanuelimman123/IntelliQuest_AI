import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastmcp import FastMCP

from backend.rag.answer_generator import RAGAnswerGenerator
from backend.agents.research_agent import ResearchAgent


mcp = FastMCP("IntelliQuest Knowledge Server")


rag = RAGAnswerGenerator()
research_agent = ResearchAgent()


@mcp.tool()
def search_documents(question: str, top_k: int = 5) -> dict:
    """
    Search uploaded PDF documents and return relevant content
    with source filenames, page numbers, and similarity scores.
    """

    if not question or not question.strip():
        return {"status": "error", "message": "Question cannot be empty"}

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        return {"status": "error", "message": "top_k must be a positive integer"}

    result = research_agent.research(
        question,
        top_k=top_k,
        min_similarity=0.40
    )

    return {
        "status": result["status"],
        "research": result["research"],
        "sources": result["sources"]
    }


@mcp.tool()
def ask_intelliquest(question: str) -> dict:
    """
    Ask a question about uploaded PDF documents and receive
    an AI-generated answer with source references.
    """

    if not question or not question.strip():
        return {"status": "error", "message": "Question cannot be empty"}

    result = rag.answer_question(
        question,
        top_k=3,
        min_similarity=0.40
    )

    return {
        "status": result["status"],
        "answer": result.get("answer"),
        "sources": result.get("sources", []),
        "message": result.get("message")
    }


if __name__ == "__main__":
    mcp.run()
