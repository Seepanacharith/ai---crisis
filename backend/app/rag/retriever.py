import re
import math
import logging
from typing import List, Dict, Any, Optional
from app.rag.vector_store import vector_store
from app.config import settings

logger = logging.getLogger("crisis_companion.rag.retriever")

class KeywordSearchEngine:
    """Simple BM25 / TF-IDF style keyword search engine for hybrid retrieval."""
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    @classmethod
    def score(cls, query: str, document_text: str) -> float:
        q_tokens = cls.tokenize(query)
        doc_tokens = cls.tokenize(document_text)
        if not q_tokens or not doc_tokens:
            return 0.0

        doc_len = len(doc_tokens)
        score = 0.0
        for token in set(q_tokens):
            count = doc_tokens.count(token)
            if count > 0:
                tf = count / doc_len
                score += (tf * (1.0 + math.log(len(token))))
        return min(score * 5.0, 1.0)


class ModularReranker:
    """Modular Reranker for re-ordering retrieved candidate chunks."""

    def __init__(self):
        self.cross_encoder = None
        try:
            from sentence_transformers import CrossEncoder
            logger.info("Initializing CrossEncoder reranker ('cross-encoder/ms-marco-MiniLM-L-6-v2')...")
            self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)
            logger.info("CrossEncoder reranker loaded.")
        except Exception as e:
            logger.warning(f"CrossEncoder unavailable: {e}. Using weighted heuristic reranker.")

    def rerank(self, query: str, candidates: List[Dict[str, Any]], top_k: int = 4) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        if self.cross_encoder:
            try:
                pairs = [[query, doc["content"]] for doc in candidates]
                scores = self.cross_encoder.predict(pairs)
                for doc, score in zip(candidates, scores):
                    doc["rerank_score"] = float(score)
                sorted_candidates = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
                return sorted_candidates[:top_k]
            except Exception as e:
                logger.error(f"CrossEncoder rerank failed: {e}")

        # Fallback weighted heuristic reranking (Vector + Keyword + Title Exact Match)
        q_lower = query.lower()
        for doc in candidates:
            vector_score = doc.get("score", 0.5)
            keyword_score = KeywordSearchEngine.score(query, doc["content"])
            
            # Boost score if disaster_type or section title matches query terms
            title_boost = 0.0
            section = doc["metadata"].get("section", "").lower()
            disaster = doc["metadata"].get("disaster_type", "").lower()
            
            if disaster in q_lower:
                title_boost += 0.15
            if any(term in section for term in q_lower.split()):
                title_boost += 0.1
                
            combined_score = (0.5 * vector_score) + (0.35 * keyword_score) + title_boost
            doc["rerank_score"] = min(combined_score, 1.0)

        sorted_candidates = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
        return sorted_candidates[:top_k]


class HybridRetriever:
    """Hybrid Retriever combining vector search and keyword search with reranking."""

    def __init__(self):
        self.reranker = ModularReranker()

    def retrieve(
        self,
        query: str,
        disaster_type: Optional[str] = "all",
        top_k: int = 10,
        rerank_top_k: int = 4
    ) -> List[Dict[str, Any]]:
        
        # 1. Vector Search Candidates
        vector_candidates = vector_store.search(
            query=query,
            top_k=top_k,
            disaster_type=disaster_type
        )
        
        # Deduplicate candidates
        candidate_dict = {}
        for cand in vector_candidates:
            cid = cand["metadata"].get("chunk_id", cand["content"][:30])
            candidate_dict[cid] = cand
            
        candidates_list = list(candidate_dict.values())
        
        # 2. Rerank candidates to select top rerank_top_k
        final_docs = self.reranker.rerank(
            query=query,
            candidates=candidates_list,
            top_k=rerank_top_k or settings.RERANK_TOP_K
        )
        
        return final_docs

hybrid_retriever = HybridRetriever()
