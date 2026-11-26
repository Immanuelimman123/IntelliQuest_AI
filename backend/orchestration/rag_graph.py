
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from backend.rag.answer_generator import RAGAnswerGenerator


class RAGState(TypedDict):

    question: str
    top_k: int
    min_similarity: float
    retrieved_chunks: list
    sources: list
    context: str
    answer: str
    status: str


class RAGWorkflow:

    def __init__(self):

        self.rag = RAGAnswerGenerator()

        workflow = StateGraph(RAGState)

        workflow.add_node("retrieve", self.retrieve_documents)
        workflow.add_node("generate", self.generate_answer)
        workflow.add_node("no_context", self.handle_no_context)

        workflow.add_edge(START, "retrieve")

        workflow.add_conditional_edges(
            "retrieve",
            self.check_relevance,
            {
                "relevant": "generate",
                "not_relevant": "no_context"
            }
        )

        workflow.add_edge("generate", END)
        workflow.add_edge("no_context", END)

        self.graph = workflow.compile()

    def retrieve_documents(self, state):

        question = state["question"]

        query_embedding = (
            self.rag.embedding_engine.generate_query_embedding(question)
        )

        chunks = self.rag.vector_store.search(
            query_embedding,
            top_k=state["top_k"],
            min_similarity=state["min_similarity"]
        )

        context_parts = []
        sources = []

        for chunk in chunks:

            metadata = chunk["metadata"]

            context_parts.append(
                f"[Source: {metadata['source']}, "
                f"Page: {metadata['page']}]\n"
                f"{chunk['text']}"
            )

            source = {
                "filename": metadata["source"],
                "page": metadata["page"],
                "similarity": chunk["similarity"]
            }

            if source not in sources:
                sources.append(source)

        return {
            "retrieved_chunks": chunks,
            "sources": sources,
            "context": "\n\n".join(context_parts)
        }

    def check_relevance(self, state):

        if state["retrieved_chunks"]:
            return "relevant"

        return "not_relevant"

    def generate_answer(self, state):

        prompt = f"""
You are IntelliQuest, an intelligent document research assistant.

Answer the user's question using only the provided document context.

Instructions:
1. Give a clear and accurate answer.
2. Do not invent information.
3. If the answer is unavailable, say so.
4. Mention source filename and page number.
5. Use simple professional language.

Document Context:
{state['context']}

User Question:
{state['question']}

Answer:
"""

        try:

            from backend.models.model_router import generate_response

            answer = generate_response(prompt)

            return {
                "answer": answer,
                "status": "success"
            }

        except Exception as e:

            print("LLM Generation Error:", str(e))

            return {
                "answer": (
                    "Document retrieval succeeded, but the "
                    "language model is temporarily unavailable."
                ),
                "status": "llm_unavailable"
            }

    def handle_no_context(self, state):

        return {
            "answer": (
                "No sufficiently relevant information was found "
                "in the uploaded documents."
            ),
            "status": "no_context"
        }

    def ask(self, question, top_k=3, min_similarity=0.40):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if not 0 <= min_similarity <= 1:
            raise ValueError("min_similarity must be between 0 and 1")

        initial_state = {
            "question": question.strip(),
            "top_k": top_k,
            "min_similarity": min_similarity,
            "retrieved_chunks": [],
            "sources": [],
            "context": "",
            "answer": "",
            "status": ""
        }

        return self.graph.invoke(initial_state)
