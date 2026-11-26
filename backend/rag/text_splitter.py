
def split_document(document, chunk_size=500, chunk_overlap=80):

    if chunk_size <= 0:
        raise ValueError("Chunk size must be positive")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("Invalid chunk overlap")

    chunks = []
    chunk_id = 0

    for page in document["pages"]:
        text = page["text"].strip()
        start = 0

        while start < len(text):

            end = min(start + chunk_size, len(text))

            if end < len(text):
                boundary = max(
                    text.rfind(" ", start, end),
                    text.rfind("\n", start, end),
                    text.rfind(".", start, end),
                    text.rfind("?", start, end)
                )

                if boundary > start + chunk_size // 2:
                    end = boundary + 1

            content = text[start:end].strip()

            if content:
                chunks.append({
                    "chunk_id": chunk_id,
                    "source": document["filename"],
                    "page": page["page"],
                    "text": content
                })

                chunk_id += 1

            if end >= len(text):
                break

            next_start = max(start + 1, end - chunk_overlap)

            # Align the next chunk with a word boundary
            while next_start < len(text) and not text[next_start].isspace():
                next_start += 1

            start = next_start

    return chunks
