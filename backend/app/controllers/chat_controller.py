import json
from typing import Optional, List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.models import User, Conversation, Message
from app.schemas.schemas import ChatRequest, ChatResponse, ConversationResponse, MessageResponse, SourceCitation
from app.rag.pipeline import rag_pipeline
from app.services.metrics_service import metrics_service

class ChatController:
    @staticmethod
    async def process_chat(
        db: AsyncSession,
        payload: ChatRequest,
        current_user: Optional[User] = None
    ) -> ChatResponse:
        
        user_id = current_user.id if current_user else "anonymous_user"
        
        # Find or create conversation thread
        conv = None
        if payload.conversation_id:
            result = await db.execute(select(Conversation).where(Conversation.id == payload.conversation_id))
            conv = result.scalars().first()
            
        if not conv and current_user:
            title_text = payload.message[:35] + "..." if len(payload.message) > 35 else payload.message
            conv = Conversation(user_id=user_id, title=title_text)
            db.add(conv)
            await db.commit()
            await db.refresh(conv)

        conv_id = conv.id if conv else "guest_conv_001"

        # Execute RAG Pipeline
        rag_result = await rag_pipeline.execute(
            query=payload.message,
            disaster_type=payload.disaster_type or "all",
            language=payload.language or "en",
            use_cache=True
        )

        # Store user and assistant messages if conversation exists
        if conv:
            user_msg = Message(
                conversation_id=conv_id,
                role="user",
                content=payload.message,
                language=payload.language or "en",
                disaster_type=payload.disaster_type
            )
            assistant_msg = Message(
                conversation_id=conv_id,
                role="assistant",
                content=rag_result["response"],
                language=payload.language or "en",
                disaster_type=payload.disaster_type,
                latency_ms=rag_result["latency"]["total_ms"],
                cache_hit=rag_result["cache_hit"],
                sources=rag_result["sources"]
            )
            db.add(user_msg)
            db.add(assistant_msg)
            await db.commit()
            assistant_msg_id = assistant_msg.id
        else:
            assistant_msg_id = "temp_msg_id"

        # Log metrics
        await metrics_service.log_metric(
            db=db,
            endpoint="/api/v1/chat",
            total_latency_ms=rag_result["latency"]["total_ms"],
            embedding_ms=rag_result["latency"]["embedding_ms"],
            retrieval_ms=rag_result["latency"]["retrieval_ms"],
            reranking_ms=rag_result["latency"]["reranking_ms"],
            llm_ms=rag_result["latency"]["llm_ms"],
            cache_hit=rag_result["cache_hit"]
        )

        sources_objs = [SourceCitation(**s) for s in rag_result["sources"]]

        return ChatResponse(
            message_id=assistant_msg_id,
            conversation_id=conv_id,
            response=rag_result["response"],
            language=rag_result["language"],
            disaster_type=rag_result["disaster_type"],
            sources=sources_objs,
            cache_hit=rag_result["cache_hit"],
            latency=rag_result["latency"]
        )

    @staticmethod
    async def process_chat_stream(
        payload: ChatRequest
    ) -> AsyncGenerator[str, None]:
        """Stream SSE formatted events for progressive UI rendering."""
        
        async for token in rag_pipeline.execute_stream(
            query=payload.message,
            disaster_type=payload.disaster_type or "all",
            language=payload.language or "en"
        ):
            event_data = json.dumps({"token": token})
            yield f"data: {event_data}\n\n"
            
        # End of stream event
        yield "data: [DONE]\n\n"

    @staticmethod
    async def get_user_history(db: AsyncSession, current_user: User) -> List[ConversationResponse]:
        result = await db.execute(
            select(Conversation)
            .where(Conversation.user_id == current_user.id)
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.created_at.desc())
        )
        conversations = result.scalars().all()
        return [ConversationResponse.model_validate(c) for c in conversations]

    @staticmethod
    async def clear_history(db: AsyncSession, current_user: User) -> bool:
        result = await db.execute(select(Conversation).where(Conversation.user_id == current_user.id))
        convs = result.scalars().all()
        for c in convs:
            await db.delete(c)
        await db.commit()
        return True

chat_controller = ChatController()
