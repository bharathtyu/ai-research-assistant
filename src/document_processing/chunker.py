class TextChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_pages(self, pages):
        """
        Split page-wise text into overlapping chunks while preserving metadata.
        """

        chunks = []
        chunk_id = 1

        for page in pages:
            page_number = page["page_number"]
            text = page["text"]

            start = 0

            while start < len(text):
                end = start + self.chunk_size

                chunk_text = text[start:end].strip()

                if chunk_text:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "page_number": page_number,
                        "text": chunk_text
                    })
                    chunk_id += 1

                start += self.chunk_size - self.chunk_overlap

        return chunks