from fastapi import APIRouter
from pydantic import BaseModel

from src.rag.qa_chain import QAChain

router = APIRouter(
    prefix="/ask",
    tags=["AI Question Answering"]
)


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 5


qa_chain = QAChain()


@router.post("/")
def ask_question(request: QuestionRequest):
    """
    Ask questions about uploaded documents.
    """

    result = qa_chain.ask(
        question=request.question,
        top_k=request.top_k
    )

    return result