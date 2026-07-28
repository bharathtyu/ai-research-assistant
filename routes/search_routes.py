from fastapi import APIRouter
from pydantic import BaseModel

from src.vector_store.manager import VectorStoreManager
from src.rag.conversation_memory import memory

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"]
)

vector_store = VectorStoreManager()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/")
async def semantic_search(request: SearchRequest):

    results = vector_store.semantic_search(
        query=request.query,
        top_k=request.top_k
    )

    formatted_results = []

    if results["documents"]:

        for i in range(len(results["documents"][0])):

            formatted_results.append(
                {
                    "document_id": results["metadatas"][0][i]["document_id"],
                    "page_number": results["metadatas"][0][i]["page_number"],
                    "chunk_id": results["metadatas"][0][i]["chunk_id"],
                    "text": results["documents"][0][i]
                }
            )

    # Save search in conversation memory
    memory.add_message(
        question=request.query,
        answer=f"Found {len(formatted_results)} relevant results."
    )

    return {
        "query": request.query,
        "results_found": len(formatted_results),
        "results": formatted_results
    }