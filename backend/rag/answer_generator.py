
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.vector_store import VectorStore
from backend.models.model_router import generate_response


class RAGAnswerGenerator:

    def __init__(self):

        self.embedding_engine = EmbeddingEngine()
        self.vector_store = VectorStore()

    def answer_question(
        self,
        question,
        top_k=3,
        min_similarity=0.25
    ):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        query_embedding = (
            self.embedding_engine.generate_query_embedding(question)
        )

        retrieved_chunks = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            min_similarity=min_similarity
        )

        if not retrieved_chunks:
            return {
                "status": "no_context",
                "answer": (
                    "No sufficiently relevant information was found "
                    "in the uploaded documents."
                ),
                "sources": [],
                "retrieved_chunks": []
            }

        context_parts = []
        sources = []

        for chunk in retrieved_chunks:

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

        context = "\n\n".join(context_parts)

        prompt = f"""
You are IntelliQuest, an intelligent document research assistant.

Answer the user's question using only the provided document context.

Instructions:
1. Give a clear and accurate answer.
2. Do not invent information.
3. If the context does not contain the answer, say so.
4. Mention the source filename and page number.
5. Use simple, professional language.
6. Organize the answer using bullet points when appropriate.

Document Context:
{context}

User Question:
{question}

Answer:
"""

        try:

            answer = generate_response(prompt)

            return {
                "status": "success",
                "answer": answer,
                "sources": sources,
                "retrieved_chunks": retrieved_chunks
            }

        except Exception as e:

            print("LLM Generation Error:", str(e))

            return {
                "status": "llm_unavailable",
                "answer": None,
                "message": (
                    "The language model is temporarily unavailable. "
                    "Document retrieval was successful."
                ),
                "sources": sources,
                "retrieved_context": context,
                "retrieved_chunks": retrieved_chunks
            }
