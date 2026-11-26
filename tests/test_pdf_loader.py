
from backend.document_processing.pdf_loader import extract_text

file_path = input("Enter PDF file path: ").strip().strip('"')

try:
    result = extract_text(file_path)

    print("\nPDF Extraction Successful!")
    print("Filename:", result["filename"])
    print("Total Pages:", result["total_pages"])
    print("\nExtracted Text Preview:")
    print(result["full_text"][:1000])

except Exception as e:
    print("PDF Extraction Failed:", e)
