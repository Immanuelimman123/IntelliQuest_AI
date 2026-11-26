
from backend.rag.embeddings import EmbeddingEngine

engine = EmbeddingEngine()

texts = [
    "Python is a high-level programming language.",
    "A list stores multiple elements.",
    "A function is a reusable block of code."
]

embeddings = engine.generate_embeddings(texts)

print("\nEmbedding Generation Successful!")
print("Number of embeddings:", len(embeddings))
print("Vector dimensions:", embeddings.shape)
print("First vector preview:", embeddings[0][:5])
