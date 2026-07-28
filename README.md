# AI Research & Knowledge Assistant

## Overview

AI Research & Knowledge Assistant is a FastAPI-based backend application that helps users upload, analyze, and interact with research documents using Artificial Intelligence. It combines semantic search, Retrieval-Augmented Generation (RAG), TensorFlow-based document classification, and conversation memory to provide intelligent document analysis.

---

## Features

- PDF Upload and Processing
- Automatic Text Extraction
- Intelligent Text Chunking
- Semantic Search using ChromaDB
- AI-powered Question Answering (RAG)
- Document Summarization
- Document Comparison
- Analytics Dashboard
- TensorFlow Document Classification
- Automatic Category Prediction
- Conversation Memory
- SQLite Database Integration
- RESTful API with FastAPI
- Interactive Swagger Documentation

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- Uvicorn

### Database
- SQLite
- SQLAlchemy

### AI & Machine Learning
- Google Gemini API
- TensorFlow
- Sentence Transformers

### Vector Database
- ChromaDB

### Other Libraries
- PyPDF2
- Scikit-learn
- NumPy
- Pandas
- Pydantic

---

## Project Structure

```
AI-RESEARCH-ASSISTANT
│
├── config/
├── data/
├── models/
├── routes/
├── src/
│   ├── database/
│   ├── document_processing/
│   ├── ml/
│   ├── rag/
│   └── vector_store/
│
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project directory

```bash
cd ai-research-assistant
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Application

```bash
uvicorn main:app --reload
```

Application URL

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Document Management

- POST `/documents/upload`
- GET `/documents/list`
- DELETE `/documents/{document_id}`
- POST `/documents/reprocess/{document_id}`

### Semantic Search

- POST `/search`

### Question Answering

- POST `/qa`

### Summarization

- POST `/summary`

### Document Comparison

- POST `/compare`

### Analytics

- GET `/analytics`

### Conversation Memory

- GET `/conversation/history`
- DELETE `/conversation/clear`

---

## AI Workflow

1. Upload PDF
2. Extract Text
3. Split into Chunks
4. Generate Embeddings
5. Store in ChromaDB
6. Perform Semantic Search
7. Retrieve Relevant Chunks
8. Generate AI Response using Gemini
9. Classify Document using TensorFlow
10. Store Conversation History

---

## Machine Learning Model

- TensorFlow Sequential Model
- Embedding Layer
- Global Average Pooling
- Dense Neural Network
- Tokenizer-based Text Processing

Categories:

- Artificial Intelligence
- Machine Learning
- Computer Vision
- Natural Language Processing
- Robotics
- Cyber Security
- Cloud Computing

---

## Future Enhancements

- User Authentication
- Persistent Conversation Memory
- Multi-user Support
- OCR for Scanned PDFs
- Advanced Analytics
- Multi-language Support

---

## Author

**Bharath Kumar Naram**

B.Tech – Information Technology

---

## License

This project is developed for educational purposes.