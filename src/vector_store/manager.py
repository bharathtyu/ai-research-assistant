import chromadb
from sentence_transformers import SentenceTransformer
import os


class VectorStoreManager:
    def __init__(self):
        """
        Initialize ChromaDB and embedding model.
        """

        self.db_path = "data/vector_db"

        os.makedirs(self.db_path, exist_ok=True)

        self.client = chromadb.PersistentClient(path=self.db_path)

        self.collection = self.client.get_or_create_collection(
            name="research_documents"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def add_chunks(self, document_id, chunks):
        """
        Store document chunks in ChromaDB.
        """

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunks:

            text = chunk["text"]

            embedding = self.embedding_model.encode(text).tolist()

            ids.append(f"{document_id}_{chunk['chunk_id']}")

            documents.append(text)

            embeddings.append(embedding)

            metadatas.append({
                "document_id": str(document_id),
                "chunk_id": chunk["chunk_id"],
                "page_number": chunk["page_number"]
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def semantic_search(self, query, top_k=5):
        """
        Search similar chunks.
        """

        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results

    def delete_document(self, document_id):
        """
        Remove all vectors of a document.
        """

        self.collection.delete(
            where={
                "document_id": str(document_id)
            }
        )