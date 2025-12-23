"""
Main entry point for the Aloysius Chatbot API.
Initializes FastAPI application with all middleware and routes.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from phase7_api.api import router
from config.config import config
from config.logging_setup import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=config.app.name,
    description="AI-powered assistant for St. Aloysius University knowledge base",
    version=config.app.version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.is_development() else ["https://staloysius.edu.in"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

# Include API routes
app.include_router(router)


@app.get("/")
def root():
    """Root endpoint with basic information"""
    return {
        "name": config.app.name,
        "version": config.app.version,
        "environment": config.app.environment,
        "docs": "/docs",
        "health": "/api/v1/health",
        "chat": "/api/v1/chat"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info(
        f"Starting {config.app.name} v{config.app.version} "
        f"in {config.app.environment} mode"
    )
    logger.info(f"Vector DB: {config.vector_db.db_path}")
    logger.info(f"Chunking: size={config.chunking.chunk_size}, "
                f"overlap={config.chunking.chunk_overlap}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down application...")


if __name__ == "__main__":
    import uvicorn
    
    logger.info(
        f"Starting server on {config.app.host}:{config.app.port} "
        f"(reload=False)"
    )
    
    uvicorn.run(
        "phase7_api.main:app",
        host=config.app.host,
        port=config.app.port,
        reload=False,
        log_level=config.logging.level.lower(),
    )
