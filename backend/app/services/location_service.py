import math
from typing import List, Dict, Any

MOCK_FACILITIES: List[Dict[str, Any]] = [
    {
        "id": "fac_01",
        "name": "Central Emergency Trauma Hospital",
        "type": "hospital",
        "address": "45 Health Avenue, Medical District",
        "phone": "+1 (800) 555-0199",
        "capacity": "150 Beds Available",
        "status": "Open 24/7",
        "latitude": 17.3850,
        "longitude": 78.4867
    },
    {
        "id": "fac_02",
        "name": "Red Cross Disaster Relief Shelter #4",
        "type": "shelter",
        "address": "102 Stadium Boulevard, North Zone",
        "phone": "+1 (800) 555-0144",
        "capacity": "450 / 600 Occupied",
        "status": "Accepting Evacuees",
        "latitude": 17.3920,
        "longitude": 78.4980
    },
    {
        "id": "fac_03",
        "name": "Metropolitan Fire & Rescue HQ",
        "type": "fire_station",
        "address": "12 Rescue Road, Central Ward",
        "phone": "101 / +1 (800) 555-0112",
        "capacity": "12 Units Deployed",
        "status": "Active Duty",
        "latitude": 17.3780,
        "longitude": 78.4750
    },
    {
        "id": "fac_04",
        "name": "Central Police Command & Dispatch",
        "type": "police",
        "address": "1 Security Plaza, Civic Center",
        "phone": "100 / +1 (800) 555-0100",
        "capacity": "Control Room Active",
        "status": "Open 24/7",
        "latitude": 17.3890,
        "longitude": 78.4810
    },
    {
        "id": "fac_05",
        "name": "St. Jude Community Evacuation Shelter",
        "type": "shelter",
        "address": "77 Hope Street, East Zone",
        "phone": "+1 (800) 555-0188",
        "capacity": "200 / 300 Occupied",
        "status": "Accepting Evacuees",
        "latitude": 17.4010,
        "longitude": 78.5120
    },
    {
        "id": "fac_06",
        "name": "Apex Specialty Hospital & Burn Center",
        "type": "hospital",
        "address": "88 Ring Road, West Ward",
        "phone": "+1 (800) 555-0177",
        "capacity": "40 ICUs Available",
        "status": "Open 24/7",
        "latitude": 17.4150,
        "longitude": 78.4450
    }
]

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2.0)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)

class LocationService:
    @staticmethod
    def get_nearby_facilities(
        user_lat: float = 17.3850,
        user_lon: float = 78.4867,
        facility_type: str = "all"
    ) -> List[Dict[str, Any]]:
        results = []
        for fac in MOCK_FACILITIES:
            if facility_type != "all" and fac["type"].lower() != facility_type.lower():
                continue
            dist = haversine_distance(user_lat, user_lon, fac["latitude"], fac["longitude"])
            item = fac.copy()
            item["distance_km"] = dist
            results.append(item)
            
        return sorted(results, key=lambda x: x["distance_km"])

location_service = LocationService()
