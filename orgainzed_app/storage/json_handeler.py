import json
from typing import Dict, Any
from pathlib import Path
from ..core.models import ScheduleManager

def save_to_json(manager: ScheduleManager, file_path: str):
    """Serialize schedule data to JSON"""
    data = {
        'courses': [c.__dict__ for c in manager.courses],
        'activities': [a.__dict__ for a in manager.activities],
        # Include other data as needed
    }
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def load_from_json(file_path: str) -> Dict[str, Any]:
    """Load schedule data from JSON"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {file_path}")
    
    with open(file_path) as f:
        return json.load(f)