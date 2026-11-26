
from backend.rag.vector_store import VectorStore


def main():

    store = VectorStore()

    records = store.collection.get(
        include=["metadatas"]
    )

    legacy_ids = []

    for record_id, metadata in zip(
        records["ids"],
        records["metadatas"]
    ):

        if not metadata.get("content_hash"):
            legacy_ids.append(record_id)

    print("\n========== LEGACY CLEANUP ==========")

    print("Total vectors:", len(records["ids"]))
    print("Legacy vectors:", len(legacy_ids))
    print("Protected hash-based vectors:",
          len(records["ids"]) - len(legacy_ids))

    if not legacy_ids:
        print("\nNo legacy records found.")
        return

    confirmation = input(
        "\nType DELETE LEGACY to continue: "
    ).strip()

    if confirmation != "DELETE LEGACY":
        print("\nCleanup cancelled.")
        return

    store.collection.delete(ids=legacy_ids)

    print("\nLegacy records deleted.")

    print("Remaining vectors:", store.collection.count())

    print("====================================")


if __name__ == "__main__":
    main()
