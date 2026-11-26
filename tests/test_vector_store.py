
from backend.document_processing.pdf_loader import extract_text
from backend.rag.text_splitter import split_document
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.vector_store import VectorStore


file_path = input("Enter PDF file path: ").strip().strip('"')

try:
    print("\nLoading PDF...")
    document = extract_text(file_path)

    print("Splitting document...")
    chunks = split_document(document, chunk_size=300, chunk_overlap=50)

    print("Generating embeddings...")
    engine = EmbeddingEngine()

    texts = [chunk["text"] for chunk in chunks]
    embeddings = engine.generate_embeddings(texts)

    print("Storing vectors in ChromaDB...")
    store = VectorStore()
    store.add_documents(chunks, embeddings)

    print("\nVector Storage Successful!")
    print("Total stored vectors:", store.collection.count())

    query = input("\nEnter your question: ")

    query_embedding = engine.generate_query_embedding(query)

    results = store.search(query_embedding, top_k=3)

    print("\nRelevant Search Results:")

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Distance:", round(result["distance"], 4))
        print("Content:", result["text"])

except Exception as e:
    print("\nVector Store Test Failed:", e)

