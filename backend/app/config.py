import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Crisis Companion"
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    
    # Security & Auth
    SECRET_KEY: str = "super-secret-crisis-companion-jwt-key-change-in-production-32-chars"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # LLM & Embeddings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = "gemini-1.5-flash"
    EMBEDDING_MODEL: str = "models/embedding-001"
    
    # Databases
    DATABASE_URL: str = "sqlite+aiosqlite:///./crisis_companion.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_PERSIST_DIR: str = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
    
    # RAG Settings
    KNOWLEDGE_BASE_DIR: str = os.path.join(os.path.dirname(__file__), "..", "..", "knowledge_base")
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RETRIEVAL: int = 10
    RERANK_TOP_K: int = 4
    
    # Caching
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
