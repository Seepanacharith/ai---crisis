from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

MOCK_ALERTS: List[Dict[str, Any]] = [
    {
        "id": "alt_101",
        "title": "FLASH FLOOD WARNING",
        "disaster_type": "flood",
        "severity": "Critical",
        "description": "Torrential monsoon downpour causing rapid water level rise in river basins and low-lying urban sectors. High inundation risk.",
        "location": "Coastal Basin Sector 4 & Central River Valleys",
        "source": "National Weather & Hydrological Bureau",
        "issued_at": (datetime.utcnow() - timedelta(minutes=25)).isoformat()
    },
    {
        "id": "alt_102",
        "title": "SEVERE CYCLONIC STORM ADVISORY",
        "disaster_type": "cyclone",
        "severity": "Warning",
        "description": "Category 3 Cyclonic Storm approaching coastal perimeter with sustained winds of 120 km/h. High wave action expected.",
        "location": "Eastern Maritime Coastal Zone",
        "source": "Maritime Hurricane Warning Center",
        "issued_at": (datetime.utcnow() - timedelta(hours=2)).isoformat()
    },
    {
        "id": "alt_103",
        "title": "EARTHQUAKE TREMOR AFTERSHOCK NOTICE",
        "disaster_type": "earthquake",
        "severity": "Advisory",
        "description": "Minor 4.2 magnitude aftershock recorded 30km epicenter depth. No structural collapse reported; stay alert for unreinforced buildings.",
        "location": "Northern Fault Line District",
        "source": "Seismological Observation Agency",
        "issued_at": (datetime.utcnow() - timedelta(hours=5)).isoformat()
    },
    {
        "id": "alt_104",
        "title": "INDUSTRIAL FOREST FIRE EVACUATION WATCH",
        "disaster_type": "fire",
        "severity": "Warning",
        "description": "Dry high-wind conditions accelerating brush fire perimeter near western forestry borders. Defensible spaces recommended.",
        "location": "Western Ridge Forestry Division",
        "source": "State Fire Management Directorate",
        "issued_at": (datetime.utcnow() - timedelta(hours=8)).isoformat()
    }
]

class AlertService:
    @staticmethod
    def get_active_alerts(disaster_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if not disaster_type or disaster_type.lower() in ["all", "none"]:
            return MOCK_ALERTS
        return [alt for alt in MOCK_ALERTS if alt["disaster_type"].lower() == disaster_type.lower()]

    @staticmethod
    def get_alert_by_id(alert_id: str) -> Optional[Dict[str, Any]]:
        for alt in MOCK_ALERTS:
            if alt["id"] == alert_id:
                return alt
        return None

alert_service = AlertService()
