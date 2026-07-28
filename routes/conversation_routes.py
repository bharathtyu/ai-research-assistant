from fastapi import APIRouter
from src.rag.conversation_memory import memory

router = APIRouter(
    prefix="/conversation",
    tags=["Conversation Memory"]
)


@router.get("/history")
def history():

    return {
        "total_messages": len(memory.get_history()),
        "history": memory.get_history()
    }


@router.delete("/clear")
def clear():

    memory.clear_history()

    return {
        "message": "Conversation history cleared successfully."
    }