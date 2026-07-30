"""
PART 6: MAIN TELEMETRY DASHBOARD & SECTOR CONTROL
Processes environment gravity drag decay calculations and prints terminal readouts.
"""

def apply_environmental_rules(current_sector, total_thrust_delivered, turn, skip_decay_once):
    """Calculates active environmental constraints on satellite performance."""
    drag_multiplier = 1.0
    salvage_rate_modifier = 0.25
    battery_generation_modifier = 1.0

    if current_sector == "Deep Space Vacuum":
        drag_multiplier = 0.40  
        battery_generation_modifier = 0.70  
    elif current_sector == "Asteroid Belt":
        drag_multiplier = 1.20  
        salvage_rate_modifier = 0.55  
    elif current_sector == "Nebula Core":
        drag_multiplier = 1.80  
        battery_generation_modifier = 1.50  

    if not skip_decay_once:
        drag_loss = min(total_thrust_delivered, (1.00 + (turn * 0.1)) * drag_multiplier)
        updated_thrust = max(0.0, total_thrust_delivered - drag_loss)
    else:
        drag_loss = 0.0
        updated_thrust = total_thrust_delivered

    return updated_thrust, drag_loss, salvage_rate_modifier, battery_generation_modifier

def show_telemetry_panel(turn, ship_class, current_sector, sector_turns_left, drag_loss, target_thrust, total_thrust_delivered, fuel_g, battery_w, max_battery, scrap, systems_health):
    """Displays clean interface analytics to tracking monitors."""
    hazard_level = "NOMINAL" if turn <= 3 else ("ELEVATED" if turn <= 7 else "CRITICAL")
    
    print(f"\n--- 🛰️ SECTOR TURN {turn} [{ship_class.upper()} | Zone: {current_sector.upper()} ({sector_turns_left} Turns Remaining)] ---")
    print(f"📊 Radiation Matrix Safety: {hazard_level}")
    if drag_loss > 0:
        print(f"📉 Environment Gravity Drag Decay: -{drag_loss:.2f} uN")
    print(f"Target Thrust Remaining: {max(0.0, target_thrust - total_thrust_delivered):.2f} uN")
    print(f"Fuel: {fuel_g:.1f}g | Battery: {battery_w:.1f}W / {max_battery}W | Scrap: {scrap}")
    print(f"Systems Health -> Prop: {systems_health['propulsion']}% | Therm: {systems_health['thermal']}% | Elec: {systems_health['electronics']}%")
