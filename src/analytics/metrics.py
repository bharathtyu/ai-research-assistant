from src.database.base import SessionLocal
from src.database.models import Document
from src.vector_store.manager import VectorStoreManager


class AnalyticsService:

    def __init__(self):
        self.vector_store = VectorStoreManager()

    def get_metrics(self):

        db = SessionLocal()

        documents = db.query(Document).all()

        total_documents = len(documents)

        processed_documents = len(
            [d for d in documents if d.processing_status == "PROCESSED"]
        )

        total_pages = sum(
            d.total_pages
            for d in documents
        )

        total_questions = sum(
            d.query_count
            for d in documents
        )

        most_queried = None

        if documents:
            top = max(
                documents,
                key=lambda d: d.query_count
            )

            most_queried = {
                "document_id": top.id,
                "document_name": top.document_name,
                "query_count": top.query_count
            }

        collection = self.vector_store.collection

        total_embeddings = collection.count()

        total_chunks = len(collection.get()["ids"])

        processing_rate = 0

        if total_documents:
            processing_rate = round(
                processed_documents / total_documents * 100,
                2
            )

        db.close()

        return {
            "total_documents": total_documents,
            "processed_documents": processed_documents,
            "total_pages": total_pages,
            "total_chunks": total_chunks,
            "total_embeddings": total_embeddings,
            "processing_success_rate": f"{processing_rate}%",
            "total_questions_answered": total_questions,
            "most_queried_document": most_queried
        }