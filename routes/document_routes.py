from fastapi import APIRouter, UploadFile, File, HTTPException
from src.database.base import SessionLocal
from src.database.models import Document
from src.document_processing.pdf_parser import PDFParser
from src.document_processing.chunker import TextChunker
from src.vector_store.manager import VectorStoreManager
from src.rag.summarizer import DocumentSummarizer
from src.rag.comparator import DocumentComparator
from src.ml.predictor import DocumentClassifier

import os
import shutil
import uuid

router = APIRouter(
    prefix="/documents",
    tags=["Document Management"]
)

UPLOAD_FOLDER = "data/raw_documents"
DATASET_FOLDER = "data/dataset"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DATASET_FOLDER, exist_ok=True)

# Initialize Vector Store
vector_store = VectorStoreManager()
summarizer = DocumentSummarizer()
comparator = DocumentComparator()

classifier = DocumentClassifier()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    # Validate PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    pdf_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save uploaded PDF
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse PDF
    parser = PDFParser(pdf_path)

    extracted_text = parser.extract_text()
    page_count = parser.get_page_count()
    pages = parser.extract_pages()

    # Save extracted text
    txt_filename = unique_filename.replace(".pdf", ".txt")
    txt_path = os.path.join(DATASET_FOLDER, txt_filename)

    with open(txt_path, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    # Predict document category
    classification = classifier.predict(extracted_text)

    predicted_category = classification["category"]
    confidence = classification["confidence"]

    print(f"Predicted Category: {predicted_category}")
    print(f"Confidence: {confidence}")

    # Create chunks
    chunker = TextChunker()
    chunks = chunker.split_pages(pages)

    # Create folder for chunk files
    chunk_folder = os.path.join(
        DATASET_FOLDER,
        unique_filename.replace(".pdf", "")
    )

    os.makedirs(chunk_folder, exist_ok=True)

    # Save chunk files
    for chunk in chunks:

        chunk_path = os.path.join(
            chunk_folder,
            f"chunk_{chunk['chunk_id']}.txt"
        )

        with open(chunk_path, "w", encoding="utf-8") as chunk_file:
            chunk_file.write(f"Chunk ID: {chunk['chunk_id']}\n")
            chunk_file.write(f"Page Number: {chunk['page_number']}\n\n")
            chunk_file.write(chunk["text"])

    # Save metadata in SQLite
    db = SessionLocal()

    new_document = Document(
        document_name=unique_filename,
        total_pages=page_count,
        processing_status="PROCESSED",
        category=predicted_category
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    db.close()

    # Store chunks in ChromaDB
    vector_store.add_chunks(
        document_id=new_document.id,
        chunks=chunks
    )

    # Response
    return {
        "message": "PDF uploaded and processed successfully",
        "document_id": new_document.id,
        "filename": unique_filename,
        "text_file": txt_filename,
        "total_pages": page_count,
        "characters_extracted": len(extracted_text),
        "chunks_created": len(chunks),
        "category": predicted_category,
        "confidence": confidence
    }
@router.get("/list")
def list_documents():

    db = SessionLocal()

    documents = db.query(Document).all()

    result = []

    for doc in documents:
        result.append(
            {
                "document_id": doc.id,
                "document_name": doc.document_name,
                "upload_time": doc.upload_time,
                "total_pages": doc.total_pages,
                "processing_status": doc.processing_status,
                "category": doc.category,
            }
        )

    db.close()

    return {
        "total_documents": len(result),
        "documents": result
    }
import glob

@router.delete("/delete/{document_id}")
def delete_document(document_id: int):

    db = SessionLocal()

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    # Delete PDF
    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        document.document_name
    )

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    # Delete extracted text
    txt_name = document.document_name.replace(".pdf", ".txt")
    txt_path = os.path.join(
        DATASET_FOLDER,
        txt_name
    )

    if os.path.exists(txt_path):
        os.remove(txt_path)

    # Delete chunk folder
    chunk_folder = os.path.join(
        DATASET_FOLDER,
        document.document_name.replace(".pdf", "")
    )

    if os.path.exists(chunk_folder):
        shutil.rmtree(chunk_folder)

    # Delete vectors
    vector_store.delete_document(document_id)

    # Delete database record
    db.delete(document)
    db.commit()
    db.close()

    return {
        "message": "Document deleted successfully.",
        "document_id": document_id
    }
@router.post("/reprocess/{document_id}")
def reprocess_document(document_id: int):

    db = SessionLocal()

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    pdf_path = os.path.join(
        UPLOAD_FOLDER,
        document.document_name
    )

    if not os.path.exists(pdf_path):
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Original PDF not found."
        )

    # Remove old vectors
    vector_store.delete_document(document_id)

    # Parse PDF again
    parser = PDFParser(pdf_path)

    extracted_text = parser.extract_text()
    pages = parser.extract_pages()
    total_pages = parser.get_page_count()

    # Save extracted text again
    txt_name = document.document_name.replace(".pdf", ".txt")
    txt_path = os.path.join(DATASET_FOLDER, txt_name)

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(extracted_text)

    # Generate chunks again
    chunker = TextChunker()
    chunks = chunker.split_pages(pages)

    # Delete old chunk folder
    chunk_folder = os.path.join(
        DATASET_FOLDER,
        document.document_name.replace(".pdf", "")
    )

    if os.path.exists(chunk_folder):
        shutil.rmtree(chunk_folder)

    os.makedirs(chunk_folder, exist_ok=True)

    # Save new chunk files
    for chunk in chunks:

        chunk_file = os.path.join(
            chunk_folder,
            f"chunk_{chunk['chunk_id']}.txt"
        )

        with open(chunk_file, "w", encoding="utf-8") as f:
            f.write(f"Chunk ID: {chunk['chunk_id']}\n")
            f.write(f"Page Number: {chunk['page_number']}\n\n")
            f.write(chunk["text"])

    # Store vectors again
    vector_store.add_chunks(
        document_id=document.id,
        chunks=chunks
    )

    # Update metadata
    document.total_pages = total_pages
    document.processing_status = "PROCESSED"

    db.commit()
    db.refresh(document)
    db.close()

    return {
        "message": "Document reprocessed successfully.",
        "document_id": document.id,
        "total_pages": total_pages,
        "chunks_created": len(chunks)
    }
@router.post("/summarize/{document_id}")
def summarize_document(
    document_id: int,
    summary_type: str = "executive"
):

    db = SessionLocal()

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    txt_path = os.path.join(
        DATASET_FOLDER,
        document.document_name.replace(".pdf", ".txt")
    )

    if not os.path.exists(txt_path):
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Extracted text file not found."
        )

    with open(txt_path, "r", encoding="utf-8") as f:
        document_text = f.read()

    db.close()

    summary = summarizer.summarize(
        document_text,
        summary_type
    )

    return {
        "document_id": document_id,
        "document_name": document.document_name,
        "summary_type": summary_type,
        "summary": summary
    }
@router.post("/compare")
def compare_documents(
    document1_id: int,
    document2_id: int
):

    db = SessionLocal()

    doc1 = db.query(Document).filter(
        Document.id == document1_id
    ).first()

    doc2 = db.query(Document).filter(
        Document.id == document2_id
    ).first()

    if not doc1 or not doc2:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="One or both documents not found."
        )

    txt1 = os.path.join(
        DATASET_FOLDER,
        doc1.document_name.replace(".pdf", ".txt")
    )

    txt2 = os.path.join(
        DATASET_FOLDER,
        doc2.document_name.replace(".pdf", ".txt")
    )

    if not os.path.exists(txt1) or not os.path.exists(txt2):
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Extracted text file missing."
        )

    with open(txt1, "r", encoding="utf-8") as f:
        document1 = f.read()

    with open(txt2, "r", encoding="utf-8") as f:
        document2 = f.read()

    db.close()

    comparison = comparator.compare(
        document1,
        document2
    )

    return {
        "document_1": doc1.document_name,
        "document_2": doc2.document_name,
        "comparison": comparison
    }