from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database.session import get_db
from app.schemas.schemas import ChecklistItem, ChecklistSaveRequest
from app.services.checklist_service import checklist_service
from app.auth.security import get_current_user_optional, get_current_user
from app.models.models import SavedChecklist, User

router = APIRouter(prefix="/checklists", tags=["Emergency Checklists"])

@router.get("/{disaster_type}", response_model=List[ChecklistItem])
async def get_checklist(
    disaster_type: str,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    if current_user:
        result = await db.execute(
            select(SavedChecklist)
            .where(SavedChecklist.user_id == current_user.id)
            .where(SavedChecklist.disaster_type == disaster_type.lower())
        )
        saved = result.scalars().all()
        if saved:
            return [
                ChecklistItem(
                    id=item.id,
                    disaster_type=item.disaster_type,
                    item=item.item,
                    completed=item.completed
                )
                for item in saved
            ]

    # Return default checklist if no saved state
    return checklist_service.get_default_checklist(disaster_type)

@router.post("", response_model=List[ChecklistItem])
async def save_checklist(
    payload: ChecklistSaveRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Clear existing items for this disaster type
    result = await db.execute(
        select(SavedChecklist)
        .where(SavedChecklist.user_id == current_user.id)
        .where(SavedChecklist.disaster_type == payload.disaster_type.lower())
    )
    for existing in result.scalars().all():
        await db.delete(existing)

    saved_items = []
    for item in payload.items:
        new_item = SavedChecklist(
            user_id=current_user.id,
            disaster_type=payload.disaster_type.lower(),
            item=item.get("item", ""),
            completed=item.get("completed", False)
        )
        db.add(new_item)
        saved_items.append(new_item)

    await db.commit()

    return [
        ChecklistItem(
            id=item.id,
            disaster_type=item.disaster_type,
            item=item.item,
            completed=item.completed
        )
        for item in saved_items
    ]
