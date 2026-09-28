import os
import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.config import settings
from app.rag.embeddings import embedding_service

logger = logging.getLogger("crisis_companion.rag.vector_store")

class ChromaVectorStore:
    def __init__(self, collection_name: str = "disaster_knowledge"):
        self.persist_dir = os.path.abspath(settings.CHROMA_PERSIST_DIR)
        os.makedirs(self.persist_dir, exist_ok=True)
        
        logger.info(f"Initializing ChromaDB client at '{self.persist_dir}'...")
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"ChromaDB collection '{self.collection_name}' ready. Count: {self.collection.count()}")

    def add_documents(self, documents: List[Dict[str, Any]]) -> None:
        if not documents:
            return
        
        ids = []
        texts = []
        metadatas = []
        
        for idx, doc in enumerate(documents):
            chunk_id = doc["metadata"].get("chunk_id", f"chunk_{idx}")
            ids.append(chunk_id)
            texts.append(doc["content"])
            metadatas.append(doc["metadata"])
            
        embeddings = embedding_service.embed_texts(texts)
        
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        logger.info(f"Successfully upserted {len(documents)} documents to ChromaDB.")

    def search(
        self,
        query: str,
        top_k: int = 10,
        disaster_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query_embedding = embedding_service.embed_query(query)
        
        where_filter = None
        if disaster_type and disaster_type.lower() not in ["all", "general", "none"]:
            where_filter = {"disaster_type": disaster_type.lower()}
            
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )
        
        retrieved = []
        if results and results["documents"] and len(results["documents"]) > 0:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0]*len(docs)
            
            for doc, meta, dist in zip(docs, metas, distances):
                # Convert distance to similarity score
                similarity = 1.0 - float(dist) if dist is not None else 0.5
                retrieved.append({
                    "content": doc,
                    "metadata": meta,
                    "score": similarity
                })
                
        return retrieved

    def count(self) -> int:
        return self.collection.count()

    def clear(self) -> None:
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

vector_store = ChromaVectorStore()
