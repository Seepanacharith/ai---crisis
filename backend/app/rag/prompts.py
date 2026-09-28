from typing import List, Dict, Any

SYSTEM_PROMPT = """You are AI Crisis Companion, an AI-powered disaster management and emergency assistance platform.

Core Operating Rules & Safety Protocols:
1. Base your answer primarily on the provided RETRIEVED EMERGENCY CONTEXT below.
2. Do NOT invent, fabricate, or assume unverified emergency procedures or contact numbers.
3. If the retrieved context does not contain sufficient details to answer the user's specific emergency query, explicitly acknowledge the limitation and provide standard safety principles.
4. Keep all responses concise, direct, clear, and highly actionable.
5. Use numbered steps or bullet points for step-by-step emergency action plans.
6. ALWAYS include an authoritative safety disclaimer reminding the user: "For active life-threatening emergencies, immediately follow instructions from official local emergency authorities and emergency services."
7. NEVER claim that you have contacted or dispatched emergency services (such as 911/112/108/fire brigade/police) on the user's behalf.
8. Clearly distinguish between general emergency preparation guidance and real-time live alert information.
9. Respond strictly in the requested LANGUAGE specified in the prompt:
   - "en" -> English
   - "hi" -> Hindi (हिंदी)
   - "te" -> Telugu (తెలుగు)

Retrieved Emergency Context:
----------------------------------------
{context}
----------------------------------------

Real-time Alert Info (if active):
{realtime_alerts}
"""

def build_prompt(
    query: str,
    retrieved_chunks: List[Dict[str, Any]],
    disaster_type: str = "all",
    language: str = "en",
    alerts_context: str = "No critical alerts active in your area."
) -> str:
    
    if retrieved_chunks:
        context_str = "\n\n".join([
            f"[Source: {chunk['metadata'].get('source', 'Unknown')} | Section: {chunk['metadata'].get('section', 'General')}]\n{chunk['content']}"
            for chunk in retrieved_chunks
        ])
    else:
        context_str = "No specific retrieved documents found for this query."

    sys_instruction = SYSTEM_PROMPT.format(
        context=context_str,
        realtime_alerts=alerts_context
    )

    lang_instruction = ""
    if language == "hi":
        lang_instruction = "\nIMPORTANT: Provide your complete response in Hindi (हिंदी)."
    elif language == "te":
        lang_instruction = "\nIMPORTANT: Provide your complete response in Telugu (తెలుగు)."

    full_prompt = f"{sys_instruction}\n\nUser Question ({disaster_type.upper()}): {query}{lang_instruction}"
    return full_prompt
