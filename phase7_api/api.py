"""
FastAPI routes for the Aloysius Chatbot.
Implements REST endpoints for chatbot interactions and health checks.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from phase7_api.schemas import ChatRequest, ChatResponse, HealthResponse
from phase7_api.rag_service import run_rag
from phase6_rag.gemini_llm import get_llm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to verify service availability.
    
    Returns:
        HealthResponse with service status
    """
    try:
        # Check Gemini API availability
        llm = get_llm()
        is_healthy = llm.health_check()
        
        if is_healthy:
            return HealthResponse(
                status="healthy",
                message="All services operational"
            )
        else:
            return HealthResponse(
                status="degraded",
                message="LLM service unavailable"
            )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            message=f"Service error: {str(e)}"
        )


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint for user queries.
    
    Args:
        request: ChatRequest containing the user's question
        
    Returns:
        ChatResponse with answer, sources, and confidence score
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Chat request received: {request.question[:100]}...")
        
        # Validate question
        if not request.question or len(request.question.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question cannot be empty"
            )
        
        # Run RAG pipeline
        answer, sources, confidence = run_rag(request.question)
        
        logger.info(f"Chat response generated - Confidence: {confidence:.2f}")
        
        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your request. Please try again."
        )


@router.get("/info")
def get_info():
    """
    Get information about the chatbot and its capabilities.
    
    Returns:
        Dictionary with chatbot information
    """
    return {
        "name": "St. Aloysius University AI Assistant",
        "version": "1.0.0",
        "description": "An AI-powered assistant for St. Aloysius University knowledge base",
        "capabilities": [
            "Answer admission questions",
            "Provide academic information",
            "Share campus facilities details",
            "Explain academic procedures",
            "Provide general university information"
        ],
        "endpoints": [
            "/api/v1/health - Health check",
            "/api/v1/chat - Send a question",
            "/api/v1/info - This endpoint"
        ]
    }
