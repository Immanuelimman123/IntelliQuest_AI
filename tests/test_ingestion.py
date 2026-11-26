
from backend.rag.ingestion import DocumentIngestion


def main():

    print("\nInitializing IntelliQuest Document Ingestion...")

    ingestion = DocumentIngestion()

    folder = input("\nEnter PDF folder path: ").strip().strip('"')

    results = ingestion.ingest_directory(folder)

    print("\n========== INGESTION REPORT ==========")

    if not results:
        print("No PDF documents found.")

    for result in results:

        print("\nDocument:", result["filename"])
        print("Status:", result["status"])

        if result["status"] in ["success", "updated"]:
            print("Pages:", result["pages"])
            print("Chunks:", result["chunks"])

        elif result["status"] == "skipped":
            print("Message:", result["message"])

        else:
            print("Error:", result["error"])

    print("\n======================================")


if __name__ == "__main__":
    main()
