"""
PART 5: SECURE HARDWARE FILE STORAGE SUB-SYSTEM
Interprets telemetry state matrices for active game data profiles.
"""
import json

SAVE_FILE = "orbital_save.json"

def write_save_state(state_dict):
    """Encodes active telemetry parameters directly to disc."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(state_dict, f)
        print("\n💾 PROGRESS SECURED: Data package transmitted to backup grid!")
        return True
    except Exception:
        print("\n❌ SYSTEM BACKUP INTERRUPTED: Internal storage stream blocked.")
        return False

def read_save_state():
    """Reads persistent vector records and extracts structured game profiles."""
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        
        required_keys = [
            "ship_class", "fuel_g", "battery_w", "max_battery", "scrap", 
            "systems_health", "total_thrust_delivered", "turn", 
            "current_sector", "sector_turns_left"
        ]
        if not all(k in data for k in required_keys):
            raise KeyError("Incomplete save format.")
        return data
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None
