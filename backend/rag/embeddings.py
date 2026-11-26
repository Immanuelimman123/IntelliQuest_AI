
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer(self.model_name)
        return self.model

    def generate_embeddings(self, texts):
        if not texts:
            return []

        model = self.load_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings

    def generate_query_embedding(self, query):
        model = self.load_model()

        return model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
