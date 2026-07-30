"""
PART 1: ENGINE CONSTANTS & SCHEMA CONFIGURATION
Defines default parameters and boundary conditions for orbital mechanics.
"""

TARGET_THRUST = 500.0

SECTORS_POOL = ["Deep Space Vacuum", "Asteroid Belt", "Nebula Core"]

SHIP_CLASSES = {
    "1": {
        "name": "Interceptor",
        "fuel": 50.0,
        "battery": 80.0,
        "max_battery": 80.0,
        "scrap": 0,
        "health": {"propulsion": 120, "thermal": 100, "electronics": 100}
    },
    "2": {
        "name": "Dreadnought",
        "fuel": 85.0,
        "battery": 100.0,
        "max_battery": 100.0,
        "scrap": 3,
        "health": {"propulsion": 100, "thermal": 100, "electronics": 100}
    },
    "3": {
        "name": "Solar Probe",
        "fuel": 40.0,
        "battery": 150.0,
        "max_battery": 150.0,
        "scrap": 0,
        "health": {"propulsion": 100, "thermal": 100, "electronics": 120}
    }
}
