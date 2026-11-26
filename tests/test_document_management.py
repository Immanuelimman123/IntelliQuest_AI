
from backend.rag.vector_store import VectorStore


def main():

    store = VectorStore()

    print("\n========== DOCUMENT MANAGEMENT ==========")

    documents = store.list_documents()

    print("\nIndexed Documents:")

    for document in documents:

        print("\nFilename:", document["filename"])
        print("Total Pages:", document["total_pages"])
        print("Total Chunks:", document["total_chunks"])

    if documents:

        filename = documents[0]["filename"]

        print("\n========== DOCUMENT DETAILS ==========")

        details = store.get_document_details(filename)

        print(details)

    print("\nTotal Vectors:", store.collection.count())

    print("\n========================================")


if __name__ == "__main__":
    main()
