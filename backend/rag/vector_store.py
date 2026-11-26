
from pathlib import Path
import chromadb


class VectorStore:

    def __init__(self, collection_name="intelliquest_documents"):

        project_root = Path(__file__).resolve().parents[2]
        storage_path = project_root / "storage" / "chroma_db"

        self.client = chromadb.PersistentClient(
            path=str(storage_path)
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def document_exists(self, content_hash, source=None):

        results = self.collection.get(
            where={"content_hash": content_hash},
            include=["metadatas"]
        )

        if source is None:
            return len(results["ids"]) > 0

        return any(
            metadata.get("source") == source
            for metadata in results["metadatas"]
        )

    def get_document_ids(self, filename):

        results = self.collection.get(
            where={"source": filename},
            include=["metadatas"]
        )

        return results["ids"]

    def delete_by_ids(self, ids):

        if ids:
            self.collection.delete(ids=ids)

    def list_documents(self):

        records = self.collection.get(
            include=["metadatas"]
        )

        documents = {}

        for metadata in records["metadatas"]:

            filename = metadata.get("source", "Unknown")

            if filename not in documents:
                documents[filename] = {
                    "filename": filename,
                    "total_chunks": 0,
                    "pages": set(),
                    "document_ids": set()
                }

            documents[filename]["total_chunks"] += 1
            documents[filename]["pages"].add(metadata.get("page"))

            if metadata.get("document_id"):
                documents[filename]["document_ids"].add(
                    metadata["document_id"]
                )

        result = []

        for document in documents.values():

            document["pages"] = sorted(
                page for page in document["pages"]
                if page is not None
            )

            document["total_pages"] = len(document["pages"])

            document["document_ids"] = list(
                document["document_ids"]
            )

            result.append(document)

        return result

    def get_document_details(self, filename):

        results = self.collection.get(
            where={"source": filename},
            include=["metadatas"]
        )

        if not results["ids"]:
            return None

        pages = sorted({
            metadata.get("page")
            for metadata in results["metadatas"]
            if metadata.get("page") is not None
        })

        document_ids = list({
            metadata.get("document_id")
            for metadata in results["metadatas"]
            if metadata.get("document_id")
        })

        content_hashes = list({
            metadata.get("content_hash")
            for metadata in results["metadatas"]
            if metadata.get("content_hash")
        })

        return {
            "filename": filename,
            "total_chunks": len(results["ids"]),
            "total_pages": len(pages),
            "pages": pages,
            "document_ids": document_ids,
            "content_hashes": content_hashes
        }

    def delete_document(self, filename):

        ids = self.get_document_ids(filename)

        self.delete_by_ids(ids)

        return len(ids)

    def add_documents(
        self,
        chunks,
        embeddings,
        document_id=None,
        content_hash=None
    ):

        if len(chunks) != len(embeddings):
            raise ValueError("Chunks and embeddings count must match")

        if not chunks:
            return

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            source = chunk["source"]
            doc_id = document_id or source

            chunk_id = (
                f"{doc_id}_"
                f"{chunk['page']}_"
                f"{chunk['chunk_id']}"
            )

            ids.append(chunk_id)
            documents.append(chunk["text"])

            metadata = {
                "source": source,
                "page": chunk["page"],
                "chunk_id": chunk["chunk_id"]
            }

            if document_id:
                metadata["document_id"] = document_id

            if content_hash:
                metadata["content_hash"] = content_hash

            metadatas.append(metadata)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )

    # Advanced semantic search with relevance filtering
    def search(self, query_embedding, top_k=3, min_similarity=0.25):

        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
            raise ValueError("top_k must be a positive integer")

        if not -1 <= min_similarity <= 1:
            raise ValueError("min_similarity must be between -1 and 1")

        total_vectors = self.collection.count()

        if total_vectors == 0:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, total_vectors),
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []

        for i in range(len(results["ids"][0])):

            distance = results["distances"][0][i]
            similarity = 1 - distance

            if similarity < min_similarity:
                continue

            retrieved.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": distance,
                "similarity": round(similarity, 4)
            })

        return retrieved
