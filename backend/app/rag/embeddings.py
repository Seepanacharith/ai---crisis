import logging
import numpy as np
from typing import List
from app.config import settings

logger = logging.getLogger("crisis_companion.rag.embeddings")

class EmbeddingService:
    def __init__(self):
        self.provider = "fallback"
        self.st_model = None
        
        # Try loading SentenceTransformers first
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Initializing SentenceTransformer ('all-MiniLM-L6-v2')...")
            self.st_model = SentenceTransformer("all-MiniLM-L6-v2")
            self.provider = "sentence_transformers"
            logger.info("SentenceTransformer loaded successfully.")
        except Exception as e:
            logger.warning(f"SentenceTransformer initialization skipped/failed: {e}")
            
        # Try Google GenAI Embeddings if key present
        if not self.st_model and settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.provider = "google"
                logger.info("Configured Google GenAI Embeddings provider.")
            except Exception as e:
                logger.warning(f"Google Embeddings setup failed: {e}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        if self.provider == "sentence_transformers" and self.st_model is not None:
            try:
                embeddings = self.st_model.encode(texts, convert_to_numpy=True)
                return embeddings.tolist()
            except Exception as e:
                logger.error(f"SentenceTransformers embedding generation error: {e}")

        if self.provider == "google" and settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                result = genai.embed_content(
                    model=settings.EMBEDDING_MODEL,
                    content=texts,
                    task_type="retrieval_document"
                )
                if "embedding" in result:
                    return [result["embedding"]] if isinstance(result["embedding"][0], float) else result["embedding"]
            except Exception as e:
                logger.error(f"Google GenAI embedding generation error: {e}")

        # Deterministic 384-dim semantic hash embedding fallback
        logger.debug("Generating fallback deterministic embeddings.")
        return [self._hash_embedding(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_texts([text])[0]

    def _hash_embedding(self, text: str, dim: int = 384) -> List[float]:
        vec = np.zeros(dim, dtype=np.float32)
        words = text.lower().split()
        for i, word in enumerate(words):
            hash_val = int(hash(word)) % dim
            vec[hash_val] += 1.0 / (i + 1)
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec.tolist()

embedding_service = EmbeddingService()
