
from backend.rag.ingestion import DocumentIngestion
from backend.database.db import SessionLocal
from backend.database.models import Document


def main():

    print("\n========== DOCUMENT METADATA TEST ==========")

    ingestion = DocumentIngestion()

    pdf_path = input("Enter PDF path: ").strip().strip('"')

    try:

        result = ingestion.ingest_pdf(pdf_path)

        print("\nIngestion Result:")
        print(result)

        db = SessionLocal()

        try:

            documents = db.query(Document).all()

            print("\n========== SQLITE DOCUMENT RECORDS ==========")

            for doc in documents:

                print("\nFilename:", doc.filename)
                print("Document ID:", doc.document_id)
                print("File Size:", doc.file_size)
                print("Pages:", doc.total_pages)
                print("Chunks:", doc.total_chunks)
                print("Status:", doc.status)

            print("\nTotal Database Records:", len(documents))

        finally:
            db.close()

    except Exception as e:

        print("\nError:", str(e))

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    main()
