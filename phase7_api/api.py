from fastapi import APIRouter
from phase7_api.schemas import ChatRequest, ChatResponse
from phase7_api.rag_service import run_rag

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer, sources = run_rag(request.question)
    return ChatResponse(answer=answer, sources=sources)
