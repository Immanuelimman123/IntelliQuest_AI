
import hashlib
from pathlib import Path

from backend.document_processing.pdf_loader import extract_text
from backend.rag.text_splitter import split_document
from backend.rag.embeddings import EmbeddingEngine
from backend.rag.vector_store import VectorStore

from backend.database.db import SessionLocal
from backend.database.models import Document


class DocumentIngestion:

    def __init__(self):
        self.embedding_engine = EmbeddingEngine()
        self.vector_store = VectorStore()

    def calculate_hash(self, file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for block in iter(lambda: file.read(65536), b""):
                sha256.update(block)

        return sha256.hexdigest()

    def save_document_metadata(
        self,
        path,
        content_hash,
        document_id,
        total_pages,
        total_chunks
    ):

        db = SessionLocal()

        try:

            document = db.query(Document).filter_by(
                filename=path.name
            ).first()

            if document:

                document.document_id = document_id
                document.content_hash = content_hash
                document.file_path = str(path.resolve())
                document.file_size = path.stat().st_size
                document.total_pages = total_pages
                document.total_chunks = total_chunks
                document.status = "completed"

            else:

                document = Document(
                    document_id=document_id,
                    filename=path.name,
                    content_hash=content_hash,
                    file_path=str(path.resolve()),
                    file_size=path.stat().st_size,
                    total_pages=total_pages,
                    total_chunks=total_chunks,
                    status="completed"
                )

                db.add(document)

            db.commit()

        except Exception:

            db.rollback()
            raise

        finally:

            db.close()

    def ingest_pdf(self, file_path):

        path = Path(file_path)

        if not path.exists() or path.suffix.lower() != ".pdf":
            raise ValueError(f"Invalid PDF file: {file_path}")

        content_hash = self.calculate_hash(path)

        if self.vector_store.document_exists(
            content_hash,
            source=path.name
        ):

            details = self.vector_store.get_document_details(
                path.name
            )

            document_id = (
                details["document_ids"][0]
                if details and details["document_ids"]
                else content_hash[:16]
            )

            self.save_document_metadata(
                path,
                content_hash,
                document_id,
                details["total_pages"] if details else 0,
                details["total_chunks"] if details else 0
            )

            return {
                "filename": path.name,
                "status": "skipped",
                "message": "Document is already up to date"
            }

        document = extract_text(path)

        if not document["pages"]:
            raise ValueError(f"No extractable text found: {path.name}")

        chunks = split_document(
            document,
            chunk_size=300,
            chunk_overlap=50
        )

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.embedding_engine.generate_embeddings(texts)

        document_id = content_hash[:16]

        old_ids = self.vector_store.get_document_ids(path.name)

        self.vector_store.add_documents(
            chunks,
            embeddings,
            document_id=document_id,
            content_hash=content_hash
        )

        self.vector_store.delete_by_ids(
            [
                old_id for old_id in old_ids
                if not old_id.startswith(document_id + "_")
            ]
        )

        self.save_document_metadata(
            path,
            content_hash,
            document_id,
            document["total_pages"],
            len(chunks)
        )

        return {
            "filename": path.name,
            "pages": document["total_pages"],
            "chunks": len(chunks),
            "status": "updated" if old_ids else "success",
            "document_id": document_id
        }

    def ingest_directory(self, directory):

        folder = Path(directory)

        if not folder.exists() or not folder.is_dir():
            raise ValueError("Invalid directory path")

        pdf_files = list(folder.glob("*.pdf"))

        results = []

        for pdf_file in pdf_files:

            try:
                results.append(self.ingest_pdf(pdf_file))

            except Exception as e:

                results.append({
                    "filename": pdf_file.name,
                    "status": "failed",
                    "error": str(e)
                })

        return results
