
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.vector_store import VectorStore


class ResearchAgent:

    def __init__(self):

        self.embedding_engine = EmbeddingEngine()
        self.vector_store = VectorStore()

    def research(self, question, top_k=5, min_similarity=0.40):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        query_embedding = (
            self.embedding_engine.generate_query_embedding(question)
        )

        chunks = self.vector_store.search(
            query_embedding,
            top_k=top_k,
            min_similarity=min_similarity
        )

        if not chunks:
            return {
                "status": "no_context",
                "research": "No relevant documents were found.",
                "sources": [],
                "chunks": []
            }

        research_results = []
        sources = []

        for chunk in chunks:

            metadata = chunk["metadata"]

            research_results.append(
                f"Source: {metadata['source']}\n"
                f"Page: {metadata['page']}\n"
                f"Similarity: {chunk['similarity']}\n"
                f"Content: {chunk['text']}"
            )

            source = {
                "filename": metadata["source"],
                "page": metadata["page"],
                "similarity": chunk["similarity"]
            }

            if source not in sources:
                sources.append(source)

        return {
            "status": "success",
            "research": "\n\n".join(research_results),
            "sources": sources,
            "chunks": chunks
        }
