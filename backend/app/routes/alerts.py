from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from app.schemas.schemas import AlertResponse
from app.services.alert_service import alert_service

router = APIRouter(prefix="/alerts", tags=["Live Disaster Alerts"])

@router.get("", response_model=List[AlertResponse])
async def get_alerts(disaster_type: Optional[str] = "all"):
    return alert_service.get_active_alerts(disaster_type)

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str):
    alt = alert_service.get_alert_by_id(alert_id)
    if not alt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID '{alert_id}' not found."
        )
    return alt
