"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    question: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User's question about the university"
    )
    
    class Config:
        example = {
            "question": "What are the admission requirements for BTech?"
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    answer: str = Field(
        ..., 
        description="AI-generated answer to the user's question"
    )
    sources: List[str] = Field(
        default=[], 
        description="URLs of sources used to generate the answer"
    )
    confidence: float = Field(
        default=0.5, 
        ge=0.0, 
        le=1.0,
        description="Confidence score of the response (0.0 to 1.0)"
    )
    
    class Config:
        example = {
            "answer": "St. Aloysius offers multiple BTech programs...",
            "sources": ["https://staloysius.edu.in/admissions"],
            "confidence": 0.85
        }


class HealthResponse(BaseModel):
    """Response schema for health check endpoint"""
    status: str = Field(
        ..., 
        description="Service status: healthy, degraded, or unhealthy"
    )
    message: str = Field(
        ..., 
        description="Detailed status message"
    )
    
    class Config:
        example = {
            "status": "healthy",
            "message": "All services operational"
        }
