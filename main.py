from fastapi import FastAPI

from src.database.base import Base, engine
from src.database.models import Document

from routes.document_routes import router as document_router
from routes.search_routes import router as search_router
from routes.analysis_routes import router as analysis_router
from routes.analytics_routes import router as analytics_router
from routes.conversation_routes import router as conversation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Research & Knowledge Assistant API",
    version="1.0.0"
)

app.include_router(document_router)
app.include_router(search_router)
app.include_router(analysis_router)
app.include_router(analytics_router)
app.include_router(conversation_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Research & Knowledge Assistant API"
    }