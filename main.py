print("Step 1")

from fastapi import FastAPI
print("Step 2")

from src.database.base import Base, engine
print("Step 3")

from src.database.models import Document
print("Step 4")

from routes.document_routes import router as document_router
print("Step 5")

from routes.search_routes import router as search_router
print("Step 6")

from routes.analysis_routes import router as analysis_router
print("Step 7")

from routes.analytics_routes import router as analytics_router
print("Step 8")

from routes.conversation_routes import router as conversation_router
print("Step 9")

Base.metadata.create_all(bind=engine)
print("Step 10")

app = FastAPI()

app.include_router(document_router)
app.include_router(search_router)
app.include_router(analysis_router)
app.include_router(analytics_router)
app.include_router(conversation_router)

print("Step 11")

@app.get("/")
def home():
    return {"message": "Welcome"}