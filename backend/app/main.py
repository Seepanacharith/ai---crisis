import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.session import init_db
from app.middleware.timing import TimingMiddleware

# Import routes
from app.routes import (
    auth,
    chat,
    disasters,
    checklists,
    alerts,
    emergency_services,
    health,
    metrics,
    admin
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("crisis_companion.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AI Crisis Companion Backend System...")
    # Initialize Database tables
    await init_db()
    
    # Auto-ingest knowledge base if Chroma vector DB is empty
    from app.rag.vector_store import vector_store
    if vector_store.count() == 0:
        logger.info("ChromaDB collection empty. Running automatic document ingestion...")
        from app.rag.loader import DocumentLoader
        from app.rag.splitter import RecursiveTextSplitter
        
        loader = DocumentLoader(settings.KNOWLEDGE_BASE_DIR)
        docs = loader.load_documents()
        if docs:
            splitter = RecursiveTextSplitter()
            chunked = splitter.split_documents(docs)
            vector_store.add_documents(chunked)
            logger.info(f"Auto-ingested {len(chunked)} chunks into vector store.")

    yield
    logger.info("Shutting down AI Crisis Companion Backend System.")

app = FastAPI(
    title=settings.APP_NAME,
    description="Production AI-Powered Disaster Management & Emergency Assistance Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(TimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration (/api/v1 prefix)
api_v1 = settings.API_V1_STR

app.include_router(auth.router, prefix=api_v1)
app.include_router(chat.router, prefix=api_v1)
app.include_router(disasters.router, prefix=api_v1)
app.include_router(checklists.router, prefix=api_v1)
app.include_router(alerts.router, prefix=api_v1)
app.include_router(emergency_services.router, prefix=api_v1)
app.include_router(health.router, prefix=api_v1)
app.include_router(metrics.router, prefix=api_v1)
app.include_router(admin.router, prefix=api_v1)

# Direct /api fallback mounts
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(disasters.router, prefix="/api")
app.include_router(checklists.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(emergency_services.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(metrics.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "title": settings.APP_NAME,
        "status": "Online",
        "docs_url": "/docs",
        "health_check": f"{api_v1}/health"
    }
