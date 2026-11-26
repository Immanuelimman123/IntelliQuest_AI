
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts):
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings

    def generate_query_embedding(self, query):
        return self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
