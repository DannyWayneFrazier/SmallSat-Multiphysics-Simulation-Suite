"""
PART 2: ORBITAL THERMODYNAMICS & PHYSICS SIMULATION
Manages mechanical tracking equations and handles component decay profiles.
"""
import random

def run_physics_turn(action, fuel_g, battery_w, current_health, turn_number, ship_class=""):
    """
    Simulates core engine tracking, orbital thermodynamics, and environmental hazards.
    Scales risks based on the current turn number indefinitely.
    """
    systems_health = current_health.copy()
    thrust_uN = 0.0
    fuel_burned_g = 0.0
    battery_change_w = 12.0  
    internal_temp_c = 20.0
    incidents = []
    propulsion_efficiency = systems_health["propulsion"] / 100.0
    
    # Infinite difficulty scaling
    hazard_multiplier = 1.0 + (turn_number // 3) * 0.03
    engine_fired = False

    # Action Processing Tree
    if action == 1:  
        if fuel_g >= 1.5 and battery_w >= 15.0:
            fuel_burned_g = 1.5
            battery_change_w = -15.0
            thrust_uN = 2.64 * propulsion_efficiency
            internal_temp_c = 162.9
            engine_fired = True
        else:
            fuel_burned_g = 0.0
            battery_change_w = -5.0  
            internal_temp_c = -35.0  
            incidents.append("🚨 POWER/FUEL FAIL: Nominal FEEP grids failed to fire! Grid drain detected.")

    elif action == 2:  
        if fuel_g >= 12.0 and battery_w >= 45.0:
            fuel_burned_g = 12.0
            battery_change_w = -45.0
            thrust_uN = 260.4 * propulsion_efficiency
            internal_temp_c = 162.9
            engine_fired = True
            
            arcing_chance = 0.25 * hazard_multiplier
            if random.random() < arcing_chance:  
                systems_health["propulsion"] = max(0, systems_health["propulsion"] - 35)
                incidents.append("💥 DIELECTRIC ARCING: 3.5 kV tension breached h-BN beds! Propulsion damaged.")
        else:
            fuel_burned_g = 0.0
            battery_change_w = -10.0  
            internal_temp_c = -35.0  
            incidents.append("🚨 POWER/FUEL FAIL: Thruster matrix choked! Major grid drain detected.")

    elif action == 3:  
        if battery_w >= 30.0:
            battery_change_w = -30.0
            internal_temp_c = 45.0  
        else:
            fuel_burned_g = 0.0
            battery_change_w = 0.0  
            internal_temp_c = -35.0  
            incidents.append("🚨 BATTERY DEPLETED: Active heating element failed to trigger!")

    elif action == 4:  
        battery_change_w = 25.0  
        internal_temp_c = -40.0  

    elif action == 5:
        battery_change_w = 12.0
        internal_temp_c = 20.0
        
    # Environmental Hazard & Misfire Tracking
    if engine_fired:
        exhaust_chance = 0.08 * hazard_multiplier
        if random.random() < exhaust_chance:
            systems_health["electronics"] = max(0, systems_health["electronics"] - 25)
            incidents.append("⚡ CNT EXHAUST FAILURE: Neutralizer misfire! Hull shocked by backscatter charge.")

    if internal_temp_c < -30.0:
        systems_health["thermal"] = max(0, systems_health["thermal"] - 30)
        incidents.append("❄️ LATTICE SHIFT: Extreme sub-zero drop caused silane bonding layers to delaminate!")

    # Cascading Failure Evaluation Tree (Patched for Dreadnought Hull passive protection)
    if turn_number > 4:
        cascade_chance = 0.15 * hazard_multiplier
        initial_turn_health = systems_health.copy()
        for component in initial_turn_health.keys():
            if 0 < systems_health[component] <= 35:
                if random.random() < cascade_chance:  
                    if ship_class == "Dreadnought":
                        incidents.append(f"🛡️ DREADNOUGHT PASSIVE: Heavy reinforced bulkheads blocked a cascading [{component.upper()}] failure!")
                    else:
                        systems_health[component] = 0
                        incidents.append(f"💀 CASCADING FAILURE: Severely degraded [{component.upper()}] array completely shorted out!")

    return {
        "fuel_burned": fuel_burned_g,
        "battery_delta": battery_change_w,
        "thrust_delivered": thrust_uN,
        "temperature": internal_temp_c,
        "incidents_logged": incidents,
        "updated_health": systems_health
    }
