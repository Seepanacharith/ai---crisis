from fastapi import APIRouter
from app.schemas.schemas import HealthStatus
from app.rag.vector_store import vector_store
from app.cache.redis_cache import disaster_cache

router = APIRouter(prefix="", tags=["Health Check"])

@router.get("/health", response_model=HealthStatus)
async def health_check():
    redis_status = "healthy" if disaster_cache.redis_client else "degraded (in-memory mode)"
    vector_status = "healthy" if vector_store.count() >= 0 else "unhealthy"
    
    return HealthStatus(
        api="healthy",
        database="healthy",
        redis=redis_status,
        vector_db=vector_status,
        llm="healthy",
        version="1.0.0"
    )
