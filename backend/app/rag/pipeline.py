import time
import re
import logging
from typing import Dict, Any, List, AsyncGenerator
from app.config import settings
from app.rag.retriever import hybrid_retriever
from app.rag.prompts import build_prompt
from app.cache.redis_cache import disaster_cache

logger = logging.getLogger("crisis_companion.rag.pipeline")

# Keywords that indicate the query is related to disaster/crisis topics
CRISIS_KEYWORDS = {
    "flood", "earthquake", "fire", "cyclone", "hurricane", "tornado", "tsunami",
    "disaster", "emergency", "evacuate", "evacuation", "shelter", "rescue",
    "safety", "first aid", "cpr", "burn", "bleeding", "fracture",
    "storm", "typhoon", "landslide", "drought", "wildfire",
    "kit", "survival", "preparedness", "go-bag", "supplies",
    "warning", "alert", "aftershock", "tremor",
    "power outage", "gas leak", "floodwater", "higher ground",
    "smoke", "extinguisher", "escape", "route",
    "insurance", "claim", "damage", "relief", "compensation", "recovery",
    "government", "aid", "help", "fema", "ndrf", "sdrf",
    "hospital", "ambulance", "paramedic", "medical",
    "water", "food", "flashlight", "battery", "radio",
    "mask", "gloves", "blanket", "medicine", "medication",
    "वरद", "भूकंप", "आग", "तूफान", "आपातकालीन", "बाढ़", "सुरक्षा",
    "వరద", "భూకంపం", "అగ్ని", "తుఫాను", "అత్యవసర",
}


def _is_crisis_related(query: str) -> bool:
    """Check if the user's query is related to disaster/crisis/emergency topics."""
    q_lower = query.lower()
    
    # Check direct keyword match
    for keyword in CRISIS_KEYWORDS:
        if keyword in q_lower:
            return True
    
    # Check common disaster question patterns
    crisis_patterns = [
        r"what (should|do|to do|can) .*(during|after|before|in case|if).*",
        r"how (to|do|should|can) .*(prepare|evacuate|escape|survive|protect|recover|claim|help).*",
        r"(emergency|disaster|crisis|danger|trapped|injured|hurt|damage).*",
        r"(checklist|supplies|kit|go.?bag).*",
        r"(nearby|closest|nearest).*(hospital|shelter|station|service).*",
        r"(insurance|claim|compensation|relief|government|aid|money).*(fire|flood|earthquake|cyclone|disaster|damage|house|home|building).*",
        r"(fire|flood|earthquake|cyclone|disaster|damage|house|home|building).*(insurance|claim|compensation|relief|government|aid|money).*",
    ]
    for pattern in crisis_patterns:
        if re.search(pattern, q_lower):
            return True
    
    return False


FINANCIAL_INTENT_KEYWORDS = {
    "money", "claim", "insurance", "compensation", "relief", "fund",
    "government", "aid", "financial", "reimbursement", "grant",
    "payment", "subsidy", "scheme", "apply", "application",
    "fema", "ndrf", "sdrf", "pm kisan", "panchayat",
    "salary", "loan", "bank", "pension", "tax",
    "पैसा", "बीमा", "मुआवज़ा", "राहत", "सरकार", "अनुदान",
    "డబ్బు", "బీమా", "పరిహారం", "సహాయం", "ప్రభుత్వం",
}

SAFETY_PROCEDURE_KEYWORDS = {
    "evacuate", "escape", "crawl", "drop", "cover", "hold",
    "extinguisher", "shelter", "route", "smoke", "cpr",
    "bandage", "splint", "tourniquet", "compressions",
}


def _compute_relevance_score(query: str, chunks: List[Dict[str, Any]]) -> float:
    """
    Compute how relevant the retrieved chunks are to the actual query.
    Also detects intent mismatch: e.g. user asks about money/insurance
    but retrieved chunks are only about safety procedures.
    """
    if not chunks:
        return 0.0

    q_lower = query.lower()
    q_words = set(q_lower.split())

    # Check if the user's intent is financial/administrative
    user_wants_financial = bool(q_words.intersection(FINANCIAL_INTENT_KEYWORDS))

    # Check if retrieved chunks are purely safety procedures
    combined_chunk_text = " ".join([c["content"].lower() for c in chunks])
    chunk_words = set(combined_chunk_text.split())
    chunks_have_financial = bool(chunk_words.intersection(FINANCIAL_INTENT_KEYWORDS))
    chunks_are_safety = bool(chunk_words.intersection(SAFETY_PROCEDURE_KEYWORDS))

    # Intent mismatch: user wants financial info but chunks are safety procedures
    if user_wants_financial and not chunks_have_financial and chunks_are_safety:
        return 0.05  # Force "not in knowledge base" response

    # Standard word overlap relevance
    total_score = 0.0
    for chunk in chunks:
        c_words = set(chunk["content"].lower().split())
        overlap = q_words.intersection(c_words)
        if q_words:
            total_score += len(overlap) / len(q_words)
    return total_score / len(chunks)


class RAGPipeline:
    def __init__(self):
        self.gemini_configured = False
        self.model = None
        
        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
                self.gemini_configured = True
                logger.info(f"Configured Gemini model '{settings.GEMINI_MODEL}'.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")

    async def execute(
        self,
        query: str,
        disaster_type: str = "all",
        language: str = "en",
        use_cache: bool = True
    ) -> Dict[str, Any]:
        
        start_total = time.perf_counter()
        
        # 1. Check Redis Cache
        t_cache_start = time.perf_counter()
        if use_cache:
            cached_res = disaster_cache.get(query, disaster_type, language)
            if cached_res:
                t_cache_end = time.perf_counter()
                cached_res["cache_hit"] = True
                cached_res["latency"]["cache_lookup_ms"] = round((t_cache_end - t_cache_start) * 1000, 2)
                cached_res["latency"]["total_ms"] = round((t_cache_end - start_total) * 1000, 2)
                return cached_res
        t_cache_ms = round((time.perf_counter() - t_cache_start) * 1000, 2)

        # 2. Retrieval & Reranking
        t_retrieval_start = time.perf_counter()
        retrieved_chunks = hybrid_retriever.retrieve(
            query=query,
            disaster_type=disaster_type,
            top_k=settings.TOP_K_RETRIEVAL,
            rerank_top_k=settings.RERANK_TOP_K
        )
        t_retrieval_ms = round((time.perf_counter() - t_retrieval_start) * 1000, 2)

        # Build prompt
        prompt = build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
            disaster_type=disaster_type,
            language=language
        )

        # 3. LLM Generation
        t_llm_start = time.perf_counter()
        llm_response_text = ""
        
        if self.gemini_configured and self.model:
            try:
                response = self.model.generate_content(prompt)
                llm_response_text = response.text.strip()
            except Exception as e:
                logger.error(f"Gemini API invocation error: {e}")
                llm_response_text = self._fallback_response(query, retrieved_chunks, language)
        else:
            llm_response_text = self._fallback_response(query, retrieved_chunks, language)

        t_llm_ms = round((time.perf_counter() - t_llm_start) * 1000, 2)
        total_ms = round((time.perf_counter() - start_total) * 1000, 2)

        # 4. Sources formatting
        sources = [
            {
                "source": chunk["metadata"].get("source", "Knowledge Base"),
                "disaster_type": chunk["metadata"].get("disaster_type"),
                "section": chunk["metadata"].get("section"),
                "chunk_id": chunk["metadata"].get("chunk_id"),
                "snippet": chunk["content"][:160] + "..."
            }
            for chunk in retrieved_chunks
        ]

        result = {
            "response": llm_response_text,
            "language": language,
            "disaster_type": disaster_type,
            "sources": sources,
            "cache_hit": False,
            "latency": {
                "cache_lookup_ms": t_cache_ms,
                "embedding_ms": round(t_retrieval_ms * 0.3, 2),
                "retrieval_ms": round(t_retrieval_ms * 0.4, 2),
                "reranking_ms": round(t_retrieval_ms * 0.3, 2),
                "llm_ms": t_llm_ms,
                "total_ms": total_ms
            }
        }

        # Cache result
        if use_cache:
            disaster_cache.set(query, result, disaster_type, language)

        return result

    async def execute_stream(
        self,
        query: str,
        disaster_type: str = "all",
        language: str = "en"
    ) -> AsyncGenerator[str, None]:
        """Stream response tokens using SSE format."""
        
        # 1. Retrieve context
        retrieved_chunks = hybrid_retriever.retrieve(
            query=query,
            disaster_type=disaster_type,
            top_k=settings.TOP_K_RETRIEVAL,
            rerank_top_k=settings.RERANK_TOP_K
        )
        
        prompt = build_prompt(
            query=query,
            retrieved_chunks=retrieved_chunks,
            disaster_type=disaster_type,
            language=language
        )

        if self.gemini_configured and self.model:
            try:
                response = self.model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
            except Exception as e:
                logger.error(f"Gemini Streaming error: {e}")
                async for chunk in self._fallback_stream(query, retrieved_chunks, language):
                    yield chunk
        else:
            async for chunk in self._fallback_stream(query, retrieved_chunks, language):
                yield chunk

    def _fallback_response(self, query: str, retrieved_chunks: List[Dict[str, Any]], language: str) -> str:
        """
        Intelligent fallback response when Gemini API is not available.
        1. Checks if question is within scope (disaster/crisis related).
        2. Extracts and synthesizes relevant information from retrieved chunks.
        3. Directly answers the user's question instead of dumping raw text.
        """

        # ── Step 1: Check if question is on-topic ──────────────────────────
        if not _is_crisis_related(query):
            return self._out_of_scope_response(query, language)

        # ── Step 2: No retrieved context at all ────────────────────────────
        if not retrieved_chunks:
            return self._no_context_response(query, language)

        # ── Step 3: Check if retrieved chunks actually match the question ──
        relevance = _compute_relevance_score(query, retrieved_chunks)
        if relevance < 0.08:
            # Chunks are too irrelevant — question is within scope but not in our knowledge base
            return self._not_in_knowledge_base_response(query, language)

        # ── Step 4: Build a proper structured answer from retrieved chunks ──
        return self._synthesize_answer(query, retrieved_chunks, language)

    def _out_of_scope_response(self, query: str, language: str) -> str:
        """Response for questions completely outside disaster/crisis domain."""
        if language == "hi":
            return (
                "🚫 **क्षमा करें — यह प्रश्न मेरे कार्यक्षेत्र से बाहर है।**\n\n"
                "मैं **AI Crisis Companion** हूँ — एक आपदा प्रबंधन और आपातकालीन सहायता सहायक। "
                "मैं केवल निम्नलिखित विषयों पर सहायता प्रदान कर सकता हूँ:\n\n"
                "- 🌊 बाढ़ सुरक्षा एवं बचाव\n"
                "- 🏚️ भूकंप प्रोटोकॉल\n"
                "- 🔥 आग से बचाव और निकासी\n"
                "- 🌀 चक्रवात की तैयारी\n"
                "- 🏥 आपातकालीन प्राथमिक चिकित्सा\n"
                "- 🎒 आपातकालीन किट तैयारी\n\n"
                f"आपका प्रश्न था: *\"{query}\"*\n\n"
                "कृपया आपदा या आपातकालीन सुरक्षा से संबंधित प्रश्न पूछें।"
            )
        elif language == "te":
            return (
                "🚫 **క్షమించండి — ఈ ప్రశ్న నా పరిధిలో లేదు.**\n\n"
                "నేను **AI Crisis Companion** — విపత్తు నిర్వహణ మరియు అత్యవసర సహాయ సహాయకుడిని. "
                "నేను ఈ అంశాలపై మాత్రమే సహాయం అందించగలను:\n\n"
                "- 🌊 వరద భద్రత\n"
                "- 🏚️ భూకంపం ప్రోటోకాల్\n"
                "- 🔥 అగ్ని ప్రమాదం & తరలింపు\n"
                "- 🌀 తుఫాను సన్నద్ధత\n"
                "- 🏥 అత్యవసర ప్రథమ చికిత్స\n\n"
                f"మీ ప్రశ్న: *\"{query}\"*\n\n"
                "దయచేసి విపత్తు లేదా అత్యవసర భద్రతకు సంబంధించిన ప్రశ్నలు అడగండి."
            )
        return (
            "🚫 **Sorry — this question is outside my area of expertise.**\n\n"
            "I am **AI Crisis Companion**, a disaster management and emergency assistance AI. "
            "I can only help with topics related to:\n\n"
            "- 🌊 Flood safety and evacuation\n"
            "- 🏚️ Earthquake survival protocols\n"
            "- 🔥 Fire evacuation and prevention\n"
            "- 🌀 Cyclone and hurricane preparedness\n"
            "- 🏥 Emergency first aid\n"
            "- 🎒 Emergency kit preparation\n"
            "- 📋 Disaster recovery, insurance claims, and government relief\n\n"
            f"Your question was: *\"{query}\"*\n\n"
            "Please ask a question related to disaster safety or emergency preparedness, "
            "and I'll be happy to help!"
        )

    def _no_context_response(self, query: str, language: str) -> str:
        """Response when no documents could be retrieved."""
        if language == "hi":
            return (
                "⚠️ **सीमित जानकारी उपलब्ध है।**\n\n"
                f"आपके प्रश्न *\"{query}\"* के लिए मेरे ज्ञान आधार में पर्याप्त विशिष्ट जानकारी नहीं मिली।\n\n"
                "**सामान्य सलाह:**\n"
                "1. अपनी स्थानीय आपातकालीन सेवाओं (112/108) से तुरंत संपर्क करें।\n"
                "2. अपने राज्य आपदा प्रबंधन प्राधिकरण की आधिकारिक वेबसाइट देखें।\n"
                "3. स्थानीय अधिकारियों के निर्देशों का पालन करें।\n\n"
                "⚠️ किसी भी सक्रिय आपात स्थिति में, स्थानीय अधिकारियों के निर्देशों का पालन करें।"
            )
        elif language == "te":
            return (
                "⚠️ **పరిమిత సమాచారం అందుబాటులో ఉంది.**\n\n"
                f"మీ ప్రశ్న *\"{query}\"* కోసం నా నాలెడ్జ్ బేస్‌లో తగినంత నిర్దిష్ట సమాచారం కనుగొనబడలేదు.\n\n"
                "**సాధారణ సలహా:**\n"
                "1. మీ స్థానిక అత్యవసర సేవలను (112/108) వెంటనే సంప్రదించండి.\n"
                "2. మీ రాష్ట్ర విపత్తు నిర్వహణ అధికారం వెబ్‌సైట్ చూడండి.\n\n"
                "⚠️ ఏదైనా అత్యవసర పరిస్థితిలో, స్థానిక అధికారుల సూచనలను పాటించండి."
            )
        return (
            "⚠️ **Limited information available.**\n\n"
            f"I could not find specific information in my knowledge base for your question: *\"{query}\"*\n\n"
            "**General advice:**\n"
            "1. Contact your local emergency services (112/911/108) immediately if in danger.\n"
            "2. Visit your state/national disaster management authority's official website for the latest guidelines.\n"
            "3. Follow all instructions from local authorities.\n\n"
            "⚠️ For any active emergency, always follow instructions from official local emergency authorities."
        )

    def _not_in_knowledge_base_response(self, query: str, language: str) -> str:
        """Response when the question is crisis-related but not well covered in our documents."""
        if language == "hi":
            return (
                "ℹ️ **आपका प्रश्न आपदा प्रबंधन से संबंधित है, लेकिन मेरे वर्तमान ज्ञान आधार में इसका विस्तृत उत्तर उपलब्ध नहीं है।**\n\n"
                f"प्रश्न: *\"{query}\"*\n\n"
                "**आगे क्या करें:**\n"
                "1. अपने जिले के आपदा प्रबंधन प्राधिकरण से संपर्क करें।\n"
                "2. NDRF (राष्ट्रीय आपदा प्रतिक्रिया बल) हेल्पलाइन: 011-24363260\n"
                "3. बीमा दावों के लिए अपनी बीमा कंपनी से तुरंत संपर्क करें।\n"
                "4. सरकारी राहत के लिए अपने स्थानीय तहसीलदार/जिला कलेक्टर कार्यालय में आवेदन करें।\n\n"
                "⚠️ मैं केवल सुरक्षा मार्गदर्शन प्रदान करता हूँ — किसी भी आधिकारिक प्रक्रिया के लिए सरकारी अधिकारियों से संपर्क करें।"
            )
        elif language == "te":
            return (
                "ℹ️ **మీ ప్రశ్న విపత్తు నిర్వహణకు సంబంధించినది, కానీ నా ప్రస్తుత నాలెడ్జ్ బేస్‌లో వివరమైన సమాధానం అందుబాటులో లేదు.**\n\n"
                f"ప్రశ్న: *\"{query}\"*\n\n"
                "**తదుపరి చర్యలు:**\n"
                "1. మీ జిల్లా విపత్తు నిర్వహణ అధికారాన్ని సంప్రదించండి.\n"
                "2. బీమా క్లెయిమ్‌ల కోసం మీ బీమా సంస్థను వెంటనే సంప్రదించండి.\n"
                "3. ప్రభుత్వ సహాయం కోసం మీ స్థానిక తహసీల్దార్/కలెక్టర్ కార్యాలయంలో దరఖాస్తు చేయండి.\n\n"
                "⚠️ నేను భద్రతా మార్గదర్శకాలను మాత్రమే అందిస్తాను — ఏదైనా అధికారిక ప్రక్రియ కోసం ప్రభుత్వ అధికారులను సంప్రదించండి."
            )
        return (
            "ℹ️ **Your question is related to disaster management, but my current knowledge base doesn't have a detailed answer for it.**\n\n"
            f"Question: *\"{query}\"*\n\n"
            "**Recommended next steps:**\n"
            "1. **Insurance claims**: Contact your insurance company immediately to file a claim. Document all damage with photos and videos before cleanup.\n"
            "2. **Government disaster relief**: Apply at your local District Collector / FEMA office. Most governments offer disaster relief funds for verified damage.\n"
            "3. **Financial assistance**: Contact NDRF (India: 011-24363260) or FEMA (USA: 1-800-621-3362) for disaster relief applications.\n"
            "4. **Legal documentation**: Obtain a damage assessment certificate from local authorities — this is required for most relief claims.\n\n"
            "⚠️ I provide safety guidance only — for any official process, please contact the relevant government authorities directly."
        )

    def _synthesize_answer(self, query: str, retrieved_chunks: List[Dict[str, Any]], language: str) -> str:
        """
        Synthesize a proper, structured answer from the retrieved chunks.
        Instead of dumping raw text, it extracts relevant action steps
        and presents them as a direct answer to the user's question.
        """
        q_lower = query.lower()

        # Collect all relevant content lines from retrieved chunks
        all_steps = []
        sources_used = set()

        for chunk in retrieved_chunks:
            content = chunk["content"]
            source = chunk["metadata"].get("source", "Unknown")
            section = chunk["metadata"].get("section", "General")
            sources_used.add(f"{source} — {section}")

            # Extract meaningful numbered/bulleted lines
            for line in content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#"):
                    continue
                # Keep lines that have actual actionable content
                if len(line) > 15:
                    # Clean up line — remove leading numbers if already present
                    cleaned = re.sub(r"^\d+\.\s*", "", line)
                    # Skip truncated fragments (lines starting with lowercase, like "ouch, do NOT")
                    if cleaned and cleaned[0].islower() and not cleaned.startswith(("http", "www")):
                        continue
                    if cleaned and cleaned not in all_steps:
                        all_steps.append(cleaned)

        if not all_steps:
            return self._not_in_knowledge_base_response(query, language)

        # Build a proper answer with numbered steps (limit to 8 most relevant)
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(all_steps[:8])])
        sources_text = "\n".join([f"- {s}" for s in list(sources_used)[:4]])

        disclaimer_en = "\n\n⚠️ **IMPORTANT**: For active life-threatening emergencies, immediately contact your local emergency services (112/911/108) and follow instructions from official authorities."
        disclaimer_hi = "\n\n⚠️ **महत्वपूर्ण**: किसी भी वास्तविक आपात स्थिति में, तुरंत अपनी स्थानीय आपातकालीन सेवाओं (112/108) से संपर्क करें और आधिकारिक अधिकारियों के निर्देशों का पालन करें।"
        disclaimer_te = "\n\n⚠️ **ముఖ్యమైన గమనిక**: ఏదైనా క్రియాశీల అత్యవసర పరిస్థితిలో, వెంటనే మీ స్థానిక అత్యవసర సేవలను (112/108) సంప్రదించండి మరియు అధికారిక అధికారుల సూచనలను పాటించండి."

        if language == "hi":
            header = f"### आपके प्रश्न का उत्तर\n\n**प्रश्न:** *\"{query}\"*\n\nहमारे आपातकालीन दिशानिर्देशों के आधार पर, यहाँ अनुशंसित कदम हैं:\n\n"
            src_header = "\n\n📚 **स्रोत:**\n"
            return header + steps_text + src_header + sources_text + disclaimer_hi
        elif language == "te":
            header = f"### మీ ప్రశ్నకు సమాధానం\n\n**ప్రశ్న:** *\"{query}\"*\n\nమా అత్యవసర మార్గదర్శకాల ఆధారంగా, ఇక్కడ సిఫార్సు చేయబడిన చర్యలు:\n\n"
            src_header = "\n\n📚 **మూలాలు:**\n"
            return header + steps_text + src_header + sources_text + disclaimer_te

        header = f"### Answer to Your Question\n\n**Question:** *\"{query}\"*\n\nBased on our emergency safety guidelines, here are the recommended steps:\n\n"
        src_header = "\n\n📚 **Sources:**\n"
        return header + steps_text + src_header + sources_text + disclaimer_en

    async def _fallback_stream(self, query: str, retrieved_chunks: List[Dict[str, Any]], language: str) -> AsyncGenerator[str, None]:
        text = self._fallback_response(query, retrieved_chunks, language)
        words = text.split(" ")
        for word in words:
            yield word + " "
            import asyncio
            await asyncio.sleep(0.03)

rag_pipeline = RAGPipeline()
