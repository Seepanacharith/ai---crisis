from fastapi import APIRouter
from typing import List, Optional
from app.schemas.schemas import EmergencyFacility
from app.services.location_service import location_service

router = APIRouter(prefix="", tags=["Emergency Services & Facilities"])

@router.get("/emergency-services", response_model=List[EmergencyFacility])
async def get_emergency_services(
    lat: float = 17.3850,
    lon: float = 78.4867,
    type: Optional[str] = "all"
):
    return location_service.get_nearby_facilities(lat, lon, type)

@router.get("/shelters", response_model=List[EmergencyFacility])
async def get_shelters(lat: float = 17.3850, lon: float = 78.4867):
    return location_service.get_nearby_facilities(lat, lon, "shelter")

@router.get("/hospitals", response_model=List[EmergencyFacility])
async def get_hospitals(lat: float = 17.3850, lon: float = 78.4867):
    return location_service.get_nearby_facilities(lat, lon, "hospital")
