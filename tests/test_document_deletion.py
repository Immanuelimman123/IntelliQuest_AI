from backend.rag.vector_store import VectorStore


def main():

    store = VectorStore()

    filename = "Delete_Test.pdf"

    print("\n========== DOCUMENT DELETION TEST ==========")

    details = store.get_document_details(filename)

    if not details:
        print("Test document not found.")
        return

    print("\nDocument found:")
    print(details)

    confirmation = input(
        f"\nType DELETE {filename} to confirm: "
    ).strip()

    if confirmation != f"DELETE {filename}":
        print("\nDeletion cancelled.")
        return

    deleted = store.delete_document(filename)

    print("\nDeleted vectors:", deleted)

    remaining = store.get_document_details(filename)

    print("Document after deletion:", remaining)

    print("Remaining total vectors:", store.collection.count())

    print("\n============================================")


if __name__ == "__main__":
    main()