
from backend.rag.vector_store import VectorStore


def main():

    store = VectorStore()

    records = store.collection.get(
        include=["metadatas"]
    )

    ids = records["ids"]
    metadatas = records["metadatas"]

    hashed = 0
    legacy = 0
    documents = {}

    for metadata in metadatas:

        source = metadata.get("source", "Unknown")

        documents[source] = documents.get(source, 0) + 1

        if metadata.get("content_hash"):
            hashed += 1
        else:
            legacy += 1

    print("\n========== DOCUMENT INVENTORY ==========")

    print("Total vectors:", len(ids))
    print("Hash-based vectors:", hashed)
    print("Legacy vectors:", legacy)

    print("\nDocument-wise records:")

    for filename, count in documents.items():
        print(f"{filename}: {count} vectors")

    print("\n========================================")


if __name__ == "__main__":
    main()
