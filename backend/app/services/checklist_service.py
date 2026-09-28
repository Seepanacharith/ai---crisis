from typing import List, Dict, Any

DEFAULT_CHECKLISTS: Dict[str, List[str]] = {
    "flood": [
        "Drinking water (1 gallon per person per day for 3 days)",
        "Non-perishable food supply (canned goods, energy bars)",
        "Waterproof flashlight with extra batteries",
        "Portable power bank (charged 100%)",
        "Important personal documents sealed in waterproof bag",
        "First-aid medical kit and essential prescription drugs",
        "Whistle to signal for emergency rescue",
        "Sturdy waterproof rain boots and change of clothing"
    ],
    "earthquake": [
        "First-aid kit with antiseptic wipes, bandages, and CPR mask",
        "Sturdy closed-toe shoes placed near bed",
        "Heavy leather gloves for clearing glass debris",
        "Emergency whistle to signal if trapped",
        "Multitool knife and pliers",
        "Water supply (3-day minimum)",
        "Flashlight and emergency radio",
        "Printed list of emergency family contacts"
    ],
    "fire": [
        "N95 particle masks or cotton cloths (smoke filtration)",
        "Working ABC fire extinguisher",
        "Go-Bag with identification documents and cash",
        "First-aid burn ointment and sterile gauze",
        "Heavy wool or flame-retardant blanket",
        "Flashlight and emergency strobe light",
        "Pet carrier and pet emergency supplies",
        "Vehicle gas tank kept filled"
    ],
    "cyclone": [
        "Battery-powered AM/FM emergency radio",
        "High-capacity USB power banks",
        "Sterilized containers filled with clean drinking water",
        "3-day non-perishable food and manual can opener",
        "Window sealing tape or plywood boards",
        "Emergency waterproof ponchos",
        "First-aid kit and chronic medications",
        "Waterproof LED lanterns"
    ]
}

class ChecklistService:
    @staticmethod
    def get_default_checklist(disaster_type: str) -> List[Dict[str, Any]]:
        items = DEFAULT_CHECKLISTS.get(disaster_type.lower(), DEFAULT_CHECKLISTS["flood"])
        return [
            {
                "id": f"{disaster_type}_{idx}",
                "disaster_type": disaster_type,
                "item": text,
                "completed": False
            }
            for idx, text in enumerate(items)
        ]

checklist_service = ChecklistService()
