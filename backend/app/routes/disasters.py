from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.schemas import DisasterGuide
from app.services.disaster_service import disaster_service

router = APIRouter(prefix="/disasters", tags=["Disaster Safety Guides"])

@router.get("", response_model=List[DisasterGuide])
async def list_disasters():
    return disaster_service.get_all_disasters()

@router.get("/{disaster_type}", response_model=DisasterGuide)
async def get_disaster(disaster_type: str):
    guide = disaster_service.get_disaster_by_type(disaster_type)
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Disaster guide for '{disaster_type}' not found."
        )
    return guide
