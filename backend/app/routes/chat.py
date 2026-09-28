from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database.session import get_db
from app.schemas.schemas import ChatRequest, ChatResponse, ConversationResponse
from app.controllers.chat_controller import chat_controller
from app.auth.security import get_current_user_optional, get_current_user
from app.middleware.rate_limiter import rate_limiter
from app.models.models import User

router = APIRouter(prefix="/chat", tags=["AI Crisis Chat"])

@router.post("", response_model=ChatResponse)
async def chat_query(
    request: Request,
    payload: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    rate_limiter.check(request)
    return await chat_controller.process_chat(db, payload, current_user)

@router.post("/stream")
async def chat_stream(
    request: Request,
    payload: ChatRequest
):
    rate_limiter.check(request)
    generator = chat_controller.process_chat_stream(payload)
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

@router.get("/history", response_model=List[ConversationResponse])
async def get_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await chat_controller.get_user_history(db, current_user)

@router.delete("/history")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await chat_controller.clear_history(db, current_user)
    return {"success": success, "message": "Chat history cleared successfully."}
