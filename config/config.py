"""
Configuration management system for the Aloysius Chatbot.
Loads environment variables from .env file and provides centralized config access.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class GeminiConfig:
    """Google Gemini API configuration"""
    api_key: str
    model: str = "gemini-2.0-flash"
    temperature: float = 0.7
    max_tokens: int = 2048
    
    def __post_init__(self):
        if not self.api_key or self.api_key == "your_google_gemini_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY not configured. "
                "Please set it in .env file or GEMINI_API_KEY environment variable."
            )


@dataclass
class VectorDBConfig:
    """Vector Database configuration"""
    db_path: str = "data/vector_db"
    collection_name: str = "aloysius_knowledge"
    persist: bool = True
    
    def __post_init__(self):
        # Create directory if it doesn't exist
        os.makedirs(self.db_path, exist_ok=True)


@dataclass
class ChunkingConfig:
    """Text chunking configuration"""
    chunk_size: int = 500
    chunk_overlap: int = 100
    min_chunk_size: int = 200
    max_chunk_size: int = 1000
    filter_navigation: bool = True
    remove_duplicates: bool = True
    min_content_length: int = 100


@dataclass
class RAGConfig:
    """Retrieval Augmented Generation configuration"""
    top_k_results: int = 5
    similarity_threshold: float = 0.6
    use_reranking: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = "INFO"
    log_file: str = "logs/app.log"
    format: str = "json"
    
    def __post_init__(self):
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)


@dataclass
class AppConfig:
    """Main application configuration"""
    name: str
    version: str
    environment: str
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class Config:
    """
    Central configuration class that loads and manages all settings.
    Provides a single source of truth for all configuration.
    """
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """Load all configuration from environment variables"""
        
        # Gemini Configuration
        try:
            self.gemini = GeminiConfig(
                api_key=os.getenv("GEMINI_API_KEY", ""),
                model=os.getenv("GEMINI_MODEL", "gemini-2.0-flash"),
            )
        except ValueError as e:
            logger.error(f"Gemini configuration error: {e}")
            raise
        
        # Vector DB Configuration
        self.vector_db = VectorDBConfig(
            db_path=os.getenv("VECTOR_DB_PATH", "data/vector_db"),
            collection_name=os.getenv("COLLECTION_NAME", "aloysius_knowledge"),
        )
        
        # Chunking Configuration
        self.chunking = ChunkingConfig(
            chunk_size=int(os.getenv("CHUNK_SIZE", "500")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "100")),
            min_chunk_size=int(os.getenv("MIN_CHUNK_SIZE", "200")),
            max_chunk_size=int(os.getenv("MAX_CHUNK_SIZE", "1000")),
            filter_navigation=os.getenv("FILTER_NAVIGATION", "true").lower() == "true",
            remove_duplicates=os.getenv("REMOVE_DUPLICATES", "true").lower() == "true",
            min_content_length=int(os.getenv("MIN_CONTENT_LENGTH", "100")),
        )
        
        # RAG Configuration
        self.rag = RAGConfig(
            top_k_results=int(os.getenv("TOP_K_RESULTS", "5")),
            similarity_threshold=float(os.getenv("SIMILARITY_THRESHOLD", "0.6")),
            use_reranking=os.getenv("USE_RERANKING", "false").lower() == "true",
        )
        
        # Logging Configuration
        self.logging = LoggingConfig(
            level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "logs/app.log"),
            format=os.getenv("LOG_FORMAT", "json"),
        )
        
        # App Configuration
        self.app = AppConfig(
            name=os.getenv("APP_NAME", "St. Aloysius University AI Assistant"),
            version=os.getenv("APP_VERSION", "1.0.0"),
            environment=os.getenv("ENVIRONMENT", "development"),
            host=os.getenv("HOST", "0.0.0.0"),
            port=int(os.getenv("PORT", "8000")),
            reload=os.getenv("RELOAD", "true").lower() == "true",
        )
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.app.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.app.environment.lower() == "development"


# Global config instance
config = Config()
