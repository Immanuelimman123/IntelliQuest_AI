from pathlib import Path
from pypdf import PdfReader


def extract_text(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    reader = PdfReader(str(path))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        content = page.extract_text()

        if content:
            pages.append({
                "page": page_number,
                "text": content.strip()
            })

    return {
        "filename": path.name,
        "total_pages": len(reader.pages),
        "pages": pages,
        "full_text": "\n".join(
            page["text"] for page in pages
        )
    }
