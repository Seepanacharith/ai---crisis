import os
import sys
import logging

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.config import settings
from app.rag.loader import DocumentLoader
from app.rag.splitter import RecursiveTextSplitter
from app.rag.vector_store import vector_store

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest_script")

def run_ingestion():
    logger.info("Starting Knowledge Base Ingestion Script...")
    kb_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
    
    loader = DocumentLoader(kb_dir)
    documents = loader.load_documents()
    
    if not documents:
        logger.error(f"No documents found in {kb_dir}")
        return

    logger.info(f"Loaded {len(documents)} raw knowledge base files.")

    splitter = RecursiveTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunked_docs = splitter.split_documents(documents)
    logger.info(f"Successfully split documents into {len(chunked_docs)} chunks.")

    logger.info("Upserting vectors and metadata into ChromaDB persistent vector store...")
    vector_store.add_documents(chunked_docs)

    logger.info(f"Ingestion complete! Total collection count in ChromaDB: {vector_store.count()}")

if __name__ == "__main__":
    run_ingestion()
