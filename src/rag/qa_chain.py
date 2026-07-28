import os

from dotenv import load_dotenv
from google import genai

from src.vector_store.manager import VectorStoreManager
from src.database.base import SessionLocal
from src.database.models import Document

load_dotenv()


class QAChain:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")

        self.client = genai.Client(api_key=api_key)
        self.vector_store = VectorStoreManager()

    def ask(self, question: str, top_k: int = 5):

        # Search relevant document chunks
        search_results = self.vector_store.semantic_search(
            question,
            top_k
        )

        documents = search_results["documents"][0]
        metadatas = search_results["metadatas"][0]

        if not documents:
            return {
                "question": question,
                "answer": "I couldn't find the answer in the uploaded documents.",
                "sources": []
            }

        # -----------------------------
        # Update query count
        # -----------------------------
        db = SessionLocal()

        updated_docs = set()

        for metadata in metadatas:

            doc_id = int(metadata["document_id"])

            if doc_id not in updated_docs:

                doc = db.query(Document).filter(
                    Document.id == doc_id
                ).first()

                if doc:
                    doc.query_count += 1

                updated_docs.add(doc_id)

        db.commit()
        db.close()

        # -----------------------------
        # Build context
        # -----------------------------
        context = "\n\n".join(documents)

        prompt = f"""
You are an AI Research Assistant.

Answer ONLY using the information provided in the context below.

If the answer is not present in the context, reply exactly:

I couldn't find the answer in the uploaded documents.

Context:
{context}

Question:
{question}

Answer:
"""

        try:
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            answer = response.text

        except Exception as e:
            return {
                "question": question,
                "answer": str(e),
                "sources": []
            }

        sources = []

        for metadata in metadatas:
            sources.append({
                "document_id": metadata["document_id"],
                "page_number": metadata["page_number"]
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }