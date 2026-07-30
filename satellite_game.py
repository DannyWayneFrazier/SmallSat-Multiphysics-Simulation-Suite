import random

def run_physics_turn(action, fuel_g, battery_w, current_health, turn_number):
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

    # 1. Action Processing Tree
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
            internal_temp_c = 20.0  
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
            internal_temp_c = 20.0  
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
        
    # 2. Environmental Hazard & Misfire Tracking
    if engine_fired:
        exhaust_chance = 0.08 * hazard_multiplier
        if random.random() < exhaust_chance:
            systems_health["electronics"] = max(0, systems_health["electronics"] - 25)
            incidents.append("⚡ CNT EXHAUST FAILURE: Neutralizer misfire! Hull shocked by backscatter charge.")

    if internal_temp_c < -30.0:
        systems_health["thermal"] = max(0, systems_health["thermal"] - 30)
        incidents.append("❄️ LATTICE SHIFT: Extreme sub-zero drop caused silane bonding layers to delaminate!")

    # 3. Cascading Failure Evaluation Tree (Grace period turn_number > 4)
    if turn_number > 4:
        cascade_chance = 0.15 * hazard_multiplier
        initial_turn_health = systems_health.copy()
        for component in initial_turn_health.keys():
            if 0 < systems_health[component] <= 35:
                if random.random() < cascade_chance:  
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

def run_repair_phase(systems_health, scrap_count):
    """Handles internal engineering bay processes for component recovery."""
    updated_health = systems_health.copy()
    while scrap_count > 0:
        if all(health >= 100 for health in updated_health.values()):
            print("\n✨ All systems operating at 100% capacity. Closing maintenance window.")
            break
            
        print(f"\n🔧 [MAINTENANCE BAY] Casing Scrap Available: {scrap_count} units")
        print(f"   🚀 Propulsion: {updated_health['propulsion']}% | 🛡️ Thermal: {updated_health['thermal']}% | ⚡ Electronics: {updated_health['electronics']}%")
        print("   Select a component to patch (Cost: 1 Scrap for +25% System Health):")
        print("   1. Patch Propulsion Modules")
        print("   2. Seal Thermal Shield Voids")
        print("   3. Recalibrate Avionics / Electronics Bus")
        print("   4. Finalize Repairs & Clear Maintenance Bay")
        
        try:
            user_input = input("\nEnter choice (1-4): ").strip()
            if not user_input:
                continue
            fix_choice = int(user_input)
            
            if fix_choice == 4:
                break
            elif fix_choice == 1:
                if updated_health["propulsion"] >= 100:
                    print("❌ Propulsion systems already operating at 100% capacity.")
                else:
                    updated_health["propulsion"] = min(100, updated_health["propulsion"] + 25)
                    scrap_count -= 1
            elif fix_choice == 2:
                if updated_health["thermal"] >= 100:
                    print("❌ Thermal shield layers already operating at 100% capacity.")
                else:
                    updated_health["thermal"] = min(100, updated_health["thermal"] + 25)
                    scrap_count -= 1
            elif fix_choice == 3:
                if updated_health["electronics"] >= 100:
                    print("❌ Electronics systems already operating at 100% capacity.")
                else:
                    updated_health["electronics"] = min(100, updated_health["electronics"] + 25)
                    scrap_count -= 1
            else:
                print("❌ Invalid choice. Please select 1-4.")
        except ValueError:
            print("❌ Input verification failed. Numeric parameter required.")
            
    return updated_health, scrap_count

def print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission, softlocked=False):
    """Computes final telemetry scores and establishes pilot flight rankings."""
    print("\n====================================================================")
    if completed_mission:
        print("🎉 MISSION SUCCESS: FLIGHT PROFILE COMPLETED SUCCESSFULLY! 🎉")
        health_sum = sum(systems_health.values())
        final_score = int((fuel_g * 5) + (battery_w * 2) + health_sum + (scrap * 50))
        
        print("-" * 68)
        print(f" 💾 PROPANE FUEL MARGIN:   {fuel_g:.1f}g  (+{int(fuel_g*5)} pts)")
        print(f" 🔋 ELECTRICAL MARGIN:     {battery_w:.1f}W  (+{int(battery_w*2)} pts)")
        print(f" 🛠️ CORES RESIDUAL HEALTH: {health_sum}/300 (+{health_sum} pts)")
        print(f" 📦 COLLECTED INVENTORY:   {scrap} Units (+{scrap*50} pts)")
        print(f" 🔥 INTEGRATED STEWARD SCORE: {final_score} POINTS")
        print("-" * 68)
        
        if final_score >= 650:
            rank = "👑🥇 ELITE FLIGHT DIRECTOR (Aerospace Legend / Perfectionist Run)"
        elif final_score >= 500:
            rank = "🥈 MISSION CONTROLLER (Senior Orbit Analyst)"
        elif final_score >= 380:
            rank = "🥉 JUNIOR SYSTEMS TECHNICIAN (Standard Qualification)"
        else:
            rank = "📉 ORBITAL HAZARD (Substandard Pass / Hazardous Re-entry Risk)"
        print(f" COMPANION FLIGHT RANK: {rank}")
    else:
        print("💀 MISSION TERMINATED: SATELLITE UNRESPONSIVE 💀")
        if softlocked:
            print(" Reason: Out of functional fuel propellant. Spacecraft drifted out of tracking bounds.")
        else:
            print(" Reason: A core hardware architecture reached critical 0% state limits.")
        print(" FINAL ACCOUNTING RANK: 🗑️ SPACE JUNK (Operational Failure)")
    print("====================================================")
def play_orbital_command():
    """Main sequence game initialization and sector turn navigation."""
    print("==================================================")
    print("        🛰️ WELCOME TO ORBITAL COMMAND v4.5 🛰️      ")
    print("==================================================")
    
    fuel_g = 65.0  # Patched fuel margin
    battery_w = 100.0
    max_battery = 100.0
    scrap = 0
    target_thrust = 500.0
    total_thrust_delivered = 0.0
    turn = 1
    
    systems_health = {
        "propulsion": 100,
        "thermal": 100,
        "electronics": 100
    }

    while total_thrust_delivered < target_thrust:
        # Patched baseline drag to make action 1 viable
        drag_loss = min(total_thrust_delivered, 1.00 + (turn * 0.1))
        total_thrust_delivered = max(0.0, total_thrust_delivered - drag_loss)

        # Space environment status alerts
        hazard_level = "NOMINAL" if turn <= 3 else ("ELEVATED" if turn <= 7 else "CRITICAL")
        
        print(f"\n--- 🛰️ SECTOR TURN {turn} [Radiation Matrix: {hazard_level}] ---")
        if drag_loss > 0:
            print(f"📉 Gravitational Drag Decay: -{drag_loss:.2f} uN")
        print(f"Target Thrust Remaining: {max(0.0, target_thrust - total_thrust_delivered):.2f} uN")
        print(f"Fuel: {fuel_g:.1f}g | Battery: {battery_w:.1f}W | Scrap: {scrap}")
        print(f"Systems Health -> Prop: {systems_health['propulsion']}% | Therm: {systems_health['thermal']}% | Elec: {systems_health['electronics']}%")

        print("\nSelect Next Sector Action:")
        print("1. Nominal Longevity FEEP Burn (Cost: 1.5g Fuel, 15W Battery | Small Thrust)")
        print("2. Emergency High-Thrust Burn  (Cost: 12.0g Fuel, 45W Battery | Huge Thrust, High Risk)")
        print("3. Engage Core Thermal Heaters (Cost: 30W Battery | Warms ship)")
        print("4. Complete Systems Shutdown   (Gains: +25W Battery | Drastic Cooling Risk)")
        print("5. Standard Standby Mode       (Gains: +12W Battery | Safe, No Thrust)")

        try:
            user_action = input("Enter action (1-5): ").strip()
            if not user_action:
                action = 5
            else:
                action = int(user_action)
                if action < 1 or action > 5:
                    print("❌ Invalid command. Satellite drifted during confusion.")
                    action = 5 
        except ValueError:
            print("❌ Verification failed. Defaulting to Standby Mode.")
            action = 5

        # 2. Physics Run Operations
        result = run_physics_turn(action, fuel_g, battery_w, systems_health, turn)
        
        fuel_g = max(0.0, fuel_g - result["fuel_burned"])
        battery_w = min(max_battery, max(0.0, battery_w + result["battery_delta"]))
        total_thrust_delivered += result["thrust_delivered"]
        systems_health = result["updated_health"]
        
        if result["incidents_logged"]:
            print("\n⚠️ TURN LOG WARNINGS:")
            for incident in result["incidents_logged"]:
                print(f"  {incident}")
        else:
            print("\n✨ Sector navigation smooth. No anomalies recorded.")

        # 3. Direct Crash Evaluation
        if any(health <= 0 for health in systems_health.values()):
            print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=False)
            return

        # 4. Salvage Event Loops
        if random.random() < 0.25:
            found_scrap = random.randint(1, 2)
            print(f"📦 ORBITAL SALVAGE: Found {found_scrap} unit(s) of usable casing scrap metal!")
            scrap += found_scrap

        # 5. Interactive Maintenance Evaluation
        if scrap > 0:
            prompt_repair = input(f"\n🔧 Scrap available ({scrap} units). Open maintenance bay? (y/n): ").strip().lower()
            if prompt_repair == 'y':
                systems_health, scrap = run_repair_phase(systems_health, scrap)

        # 6. Structural Soft-Lock Detection
        if fuel_g < 1.5 and total_thrust_delivered < target_thrust:
            print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=False, softlocked=True)
            return

        turn += 1

    print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=True)

if __name__ == "__main__":
    play_orbital_command()
