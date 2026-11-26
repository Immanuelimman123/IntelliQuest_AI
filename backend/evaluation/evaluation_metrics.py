
import numpy as np

from backend.rag.embeddings import EmbeddingEngine


class EvaluationMetrics:

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()

    def semantic_similarity(self, text1, text2):

        if not text1.strip() or not text2.strip():
            return 0.0

        embeddings = self.embedding_engine.generate_embeddings(
            [text1, text2]
        )

        similarity = np.dot(
            embeddings[0],
            embeddings[1]
        )

        return float(np.clip(similarity, 0.0, 1.0))

    def evaluate_answer(
        self,
        question,
        answer,
        retrieved_chunks
    ):

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        if not answer or not answer.strip():
            raise ValueError("Answer cannot be empty")

        if not retrieved_chunks:
            raise ValueError("No retrieved context available")

        context_texts = [
            chunk["text"]
            for chunk in retrieved_chunks
            if chunk.get("text")
        ]

        if not context_texts:
            raise ValueError("Retrieved context is empty")

        context = "\n".join(context_texts)

        answer_relevance = self.semantic_similarity(
            question,
            answer
        )

        context_relevance = self.semantic_similarity(
            question,
            context
        )

        answer_context_alignment = self.semantic_similarity(
            answer,
            context
        )

        retrieval_scores = [
            chunk["similarity"]
            for chunk in retrieved_chunks
            if "similarity" in chunk
        ]

        retrieval_quality = (
            sum(retrieval_scores) / len(retrieval_scores)
            if retrieval_scores
            else 0.0
        )

        return {
            "answer_relevance": round(answer_relevance, 4),
            "context_relevance": round(context_relevance, 4),
            "answer_context_alignment": round(
                answer_context_alignment, 4
            ),
            "retrieval_quality": round(retrieval_quality, 4)
        }
