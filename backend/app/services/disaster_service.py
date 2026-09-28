from typing import List, Dict, Any, Optional

DISASTER_GUIDES: Dict[str, Dict[str, Any]] = {
    "flood": {
        "type": "flood",
        "title": "Flood Emergency Response Guide",
        "overview": "Floods occur due to torrential rains, storm surges, or dam breaches. Immediate evacuation to elevated ground is essential.",
        "before": [
            "Prepare a 72-hour emergency Go-Bag with non-perishable food, water, flashlight, and first-aid supplies.",
            "Elevate critical household appliances and electrical panels above potential flood lines.",
            "Keep important documents in waterproof sealed bags.",
            "Know your local high-ground evacuation routes."
        ],
        "during": [
            "Move immediately to higher ground or upper floors of sturdy structures.",
            "NEVER walk, swim, or drive through moving floodwaters (12 inches can sweep away cars).",
            "Turn off main electricity, gas, and water supplies if instructed.",
            "Avoid contact with floodwater due to contamination and live electrical wire hazards."
        ],
        "after": [
            "Return home only when local emergency authorities declare it safe.",
            "Inspect building structures for cracks before entering.",
            "Drink only bottled or boiled water until municipal supplies are verified safe.",
            "Discard all food that came in contact with floodwater."
        ],
        "icon": "Waves"
    },
    "earthquake": {
        "type": "earthquake",
        "title": "Earthquake Survival & Safety Guide",
        "overview": "Earthquakes strike without warning. Practicing 'Drop, Cover, and Hold On' immediately saves lives.",
        "before": [
            "Anchor tall, heavy furniture, bookshelves, and appliances to wall studs.",
            "Secure heavy wall fixtures and mirrors away from beds.",
            "Establish an emergency family meeting location outdoors.",
            "Assemble a sturdy Go-Bag with first-aid items and sturdy footwear."
        ],
        "during": [
            "DROP onto your hands and knees immediately.",
            "COVER your head and neck under a sturdy desk or table.",
            "HOLD ON to your shelter until all shaking stops completely.",
            "If outdoors, move away from buildings, streetlights, and power lines."
        ],
        "after": [
            "Be prepared for secondary aftershocks.",
            "Check for injuries and administer first aid.",
            "Inspect home for gas leaks; if smelled, turn off main valve and evacuate.",
            "Do NOT use elevators or light matches if gas leaks are suspected."
        ],
        "icon": "Activity"
    },
    "fire": {
        "type": "fire",
        "title": "Building Fire & Wildfire Evacuation Guide",
        "overview": "Fires spread rapidly and create lethal toxic smoke. Rapid evacuation and crawling low save lives.",
        "before": [
            "Install smoke detectors on every floor and test them monthly.",
            "Keep working ABC fire extinguishers near kitchen and exit doors.",
            "Identify two escape routes from every room in your residence.",
            "Create a 30-foot defensible brush-free space around homes in wildfire zones."
        ],
        "during": [
            "GET OUT AND STAY OUT immediately. Never return for belongings.",
            "Crawl low under smoke where air is cleaner and cooler.",
            "Test door handles with the back of your hand before opening.",
            "If clothing catches fire: STOP, DROP, AND ROLL until flames are out."
        ],
        "after": [
            "Do not re-enter burned structures until fire officials give clearance.",
            "Wear heavy boots, N95 masks, and gloves during debris inspection.",
            "Document property damage for insurance before starting cleanup.",
            "Watch out for hot embers and weak overhead roof beams."
        ],
        "icon": "Flame"
    },
    "cyclone": {
        "type": "cyclone",
        "title": "Tropical Cyclone & Storm Survival Guide",
        "overview": "Cyclones bring destructive winds, extreme rain, and severe coastal storm surges.",
        "before": [
            "Monitor official weather broadcasts and cyclone warning bulletins.",
            "Board up glass windows or close storm shutters.",
            "Secure outdoor furniture, trash bins, and loose roof panels.",
            "Charge mobile phones, power banks, and battery emergency radios."
        ],
        "during": [
            "Remain inside a safe, windowless interior room or hallway.",
            "Disconnect non-essential electrical appliances.",
            "Do NOT venture outside during the 'eye' of the cyclone when winds temporarily calm.",
            "Keep listening to battery-operated radios for emergency alerts."
        ],
        "after": [
            "Stay clear of downed power lines and standing water.",
            "Beware of unstable trees and structural damage.",
            "Boil tap water before drinking.",
            "Use flashlights instead of open candle flames."
        ],
        "icon": "Wind"
    }
}

class DisasterService:
    @staticmethod
    def get_all_disasters() -> List[Dict[str, Any]]:
        return list(DISASTER_GUIDES.values())

    @staticmethod
    def get_disaster_by_type(disaster_type: str) -> Optional[Dict[str, Any]]:
        return DISASTER_GUIDES.get(disaster_type.lower())

disaster_service = DisasterService()
