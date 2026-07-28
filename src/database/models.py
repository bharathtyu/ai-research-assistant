from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from src.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False)
    upload_time = Column(DateTime, default=datetime.utcnow)
    total_pages = Column(Integer, default=0)
    processing_status = Column(String, default="PENDING")
    category = Column(String, default="Unknown")

    # NEW
    query_count = Column(Integer, default=0)