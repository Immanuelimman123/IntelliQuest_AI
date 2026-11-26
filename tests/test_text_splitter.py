
from backend.document_processing.pdf_loader import extract_text
from backend.rag.text_splitter import split_document

file_path = input("Enter PDF file path: ").strip().strip('"')

try:
    document = extract_text(file_path)

    chunks = split_document(
        document,
        chunk_size=300,
        chunk_overlap=50
    )

    print("\nText Chunking Successful!")
    print("Document:", document["filename"])
    print("Total Chunks:", len(chunks))

    for chunk in chunks:
        print("\n------------------------------")
        print("Chunk ID:", chunk["chunk_id"])
        print("Page:", chunk["page"])
        print("Content:", chunk["text"])

except Exception as e:
    print("Chunking Failed:", e)
