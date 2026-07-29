import random
import sys

# ====================================================================
#   AUDITED PHYSICS CORE & COMPONENT STATE MACHINE
# ====================================================================

def run_physics_turn(action, fuel_g, battery_w, systems_health):
    """
    Advanced Physics Core Matrix v4.0.0. Evaluates resource limitations,
    tracks dynamic electronics battery caps, and monitors component degradation.
    """
    thrust_uN = 0.0
    fuel_burned_g = 0.0
    battery_change_w = 12.0  # Base solar array recovery rate per sector
    internal_temp_c = 20.0
    incidents = []
    
    propulsion_efficiency = systems_health["propulsion"] / 100.0

    # FIX: Strict resource pre-check gates prevent infinite negative execution loops
    if action == 1:  # Nominal Longevity FEEP Burn
        if fuel_g >= 1.5 and battery_w >= 15.0:
            fuel_burned_g = 1.5
            battery_change_w = -15.0
            thrust_uN = 2.64 * propulsion_efficiency
            internal_temp_c = 162.9
        else:
            action = 0  # Re-route to system failure mode
            incidents.append("🚨 POWER/FUEL FAIL: Nominal FEEP grids failed to fire! Thrust flatlined.")

    elif action == 2:  # Emergency High-Thrust Burn
        if fuel_g >= 12.0 and battery_w >= 45.0:
            fuel_burned_g = 12.0
            battery_change_w = -45.0
            thrust_uN = 260.4 * propulsion_efficiency
            internal_temp_c = 162.9
            
            # Dielectric arcing threshold check from your verified FEEP schematic
            if random.random() < 0.25:  
                systems_health["propulsion"] = max(0, systems_health["propulsion"] - 35)
                incidents.append("💥 DIELECTRIC ARCING: 3.5 kV tension breached h-BN beds! Propulsion damaged.")
        else:
            action = 0
            incidents.append("🚨 POWER/FUEL FAIL: Thruster matrix choked! Trajectory correction failed.")

    elif action == 3:  # Activate Honeycomb Shield Heaters
        if battery_w >= 30.0:
            battery_change_w = -30.0
            internal_temp_c = 45.0  # Safe phase-change plateau from your code
        else:
            action = 0
            incidents.append("🚨 BATTERY DEPLETED: Active heating element failed to trigger!")
            internal_temp_c = -50.0

    elif action == 4:  # Complete Systems Cold Shut-down
        battery_change_w = 25.0  
        internal_temp_c = -40.0  # Severe radiative cooling down to deep space sink
        
    # Check CNT Neutralizer electrical loops if high-voltage systems fired
    if action in:
        if random.random() < 0.08:
            systems_health["electronics"] = max(0, systems_health["electronics"] - 25)
            incidents.append("⚡ CNT EXHAUST FAILURE: Neutralizer misfire! Spacecraft hull shocked by backscatter charge.")

    # Check thermal expansion structural boundaries from shield script
    if internal_temp_c < -30.0:
        systems_health["thermal"] = max(0, systems_health["thermal"] - 30)
        incidents.append("❄️ LATTICE SHIFT: Extreme sub-zero drop caused silane bonding layers to delaminate!")

    # EXPANSION: Critical state damage propagation rules
    for component, health in systems_health.items():
        if 0 < health <= 35:
            if random.random() < 0.15:  # 15% cascading failure risk under heavy strain
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
    """
    Locked-down Maintenance Loop. Fixes exploits to ensure scrap 
    is only deducted upon a valid, safe system restoration.
    """
    while scrap_count > 0:
        print(f"\n🔧 [MAINTENANCE BAY] Casing Scrap Available: {scrap_count} units")
        print(f"   🚀 Propulsion: {systems_health['propulsion']}% | 🛡️ Thermal: {systems_health['thermal']}% | ⚡ Electronics: {systems_health['electronics']}%")
        print("   Select a component to patch (Cost: 1 Scrap for +25% System Health):")
        print("   1. Patch Propulsion Modules")
        print("   2. Seal Thermal Shield Voids")
        print("   3. Recalibrate Avionics / Electronics Bus")
        print("   4. Finalize Repairs & Clear Maintenance Bay")
        
        try:
            fix_choice = int(input("\nEnter choice (1-4): "))
            if fix_choice == 4:
                break
            elif fix_choice == 1:
                if systems_health["propulsion"] >= 100:
                    print("❌ Propulsion systems already operating at 100% capacity.")
                else:
                    systems_health["propulsion"] = min(100, systems_health["propulsion"] + 25)
                    scrap_count -= 1
            elif fix_choice == 2:
                if systems_health["thermal"] >= 100:
                    print("❌ Thermal shield layers already operating at 100% capacity.")
                else:
                    systems_health["thermal"] = min(100, systems_health["thermal"] + 25)
                    scrap_count -= 1
            elif fix_choice == 3:
                if systems_health["electronics"] >= 100:
                    print("❌ Electronics systems already operating at 100% capacity.")
                else:
                    systems_health["electronics"] = min(100, systems_health["electronics"] + 25)
                    scrap_count -= 1
            else:
                print("❌ Invalid command parameter input. Choose a sector choice from 1 to 4.")
        except ValueError:
            print("❌ Input verification failed. Numeric parameter required.")
            
    return systems_health, scrap_count

# ====================================================================
#   THE AEROSPACE SCOREBOARD RANKING MATRIX
# ====================================================================

def print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission):
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
        
        if final_score >= 750:
            rank = "👑🥇 ELITE FLIGHT DIRECTOR (Aerospace Legend / Perfectionist Run)"
        elif final_score >= 550:
            rank = "🥈 MISSION CONTROLLER (Senior Orbit Analyst)"
        elif final_score >= 380:
            rank = "🥉 JUNIOR SYSTEMS TECHNICIAN (Standard Qualification)"
        else:
            rank = "📉 ORBITAL HAZARD (Substandard Pass / Hazardous Re-entry Risk)"
            
        print(f" COMPANION FLIGHT RANK: {rank}")
    else:
        print("💀 MISSION TERMINATED: SATELLITE UNRESPONSIVE 💀")
        print(" Reason: A core hardware architecture reached critical 0% state limits.")
        print(" FINAL ACCOUNTING RANK: 🗑️ SPACE JUNK (Operational Failure)")
    print("====================================================================\n")

# ====================================================================
#   MAIN GAME ACTION SYSTEM LOOP
# ====================================================================

def play_orbital_command():
    print("====================================================================")
    print("      🚀 ORBITAL COMMAND: SATELLITE SURVIVAL SIMULATOR v4.0.0 🚀     ")
    print("====================================================================")
    print(" OBJECTIVE: Navigate 6 hazardous orbit tracking sectors in sequence.")
    print(" SYSTEM RULES: Component health strictly limits maximum battery load.")
    print("====================================================================\n")

    fuel_g = 100.0
    battery_w = 100.0
    scrap = 0
    current_cycle = 1
    total_cycles = 6
    completed_mission = False
    
    systems_health = {"propulsion": 100, "thermal": 100, "electronics": 100}

    events = {
        1: "⚠️ SATELLITE DEBRIS ALARM: A cloud of dead engine shards is hurtling toward your current altitude window!",
        2: "🌑 THERMAL ECLIPSE: Entering Earth's shadow segment. Solar cells blacked out. Extreme structural radiation loss activated.",
        3: "💨 THERMOSPHERIC DRAG WAVE: Solar radiation flare expands air drag. Trajectory vector rapidly decaying down.",
        4: "📡 ABANDONED PROBE: Trajectory crosses an old, defunct military probe. High-gain tracking indicates salvage potential.",
        5: "☀️ GEOMAGNETIC SURGE: A high-density ion shockwave is bombarding your primary electrical distribution bus.",
        6: "🏁 TERMINAL ORBIT TRACKING: Final telemetry gateway sequence. Lock down active position configurations."
    }

    while current_cycle <= total_cycles:
        # Check explicit modular failure game over codes
        if any(health <= 0 for health in systems_health.values()):
            completed_mission = False
            break
            
        # EXPANSION: Battery Storage Limit linked dynamically to Avionics Bus stability
        max_battery_capacity = max(15.0, systems_health["electronics"])
        if battery_w > max_battery_capacity:
            battery_w = max_battery_capacity

        print(f"\n▶️ [ORBIT SECTOR {current_cycle} / {total_cycles}]")
        print(f"  🔋 Fuel Mass: {fuel_g:.1f}g | ⚡ Battery: {battery_w:.1f}W / {max_battery_capacity:.1f}W (Cap) | 📦 Inventory: {scrap} Scrap")
        print(f"  🛠️ Subsystems -> 🚀 Prop: {systems_health['propulsion']}% | 🛡️ Therm: {systems_health['thermal']}% | ⚡ Elec: {systems_health['electronics']}%")
        print("-" * 78)
        print(events[current_cycle])
        print("-" * 78)

        print(" INITIATE COMMAND SEQUENCE OPTION:")
        print("  1. Fire FEEP Thrusters: Longevity Profile (Consumes 1.5g Fuel, 15W Power)")
        print("  2. Fire FEEP Thrusters: High-Thrust Profile (Consumes 12.0g Fuel, 45W Power)")
        print("  3. Engage Active Honeycomb Core Thermal Heaters (Consumes 30W Power)")
        print("  4. Route System to Cold Passive Sleep State (Recovers 25W Power, Drops Core Temp)")
        
        while True:
            try:
                choice = int(input("\nEnter instruction command integer (1-4): "))
                if choice in: 
                    break
                print("❌ Selection out of bounds. Choose an action vector from 1 to 4.")
            except ValueError:
                print("❌ Input processing failure. Integer scalar required.")

        # Compute Turn Results through Physics Engine
        result = run_physics_turn(choice, fuel_g, battery_w, systems_health)

        # Update primary metrics registers safely
        fuel_g = max(0.0, fuel_g - result["fuel_burned"])
        battery_w = min(max_battery_capacity, max(0.0, battery_w + result["battery_delta"]))
        systems_health = result["updated_health"]

        print("\n⚙️ PROCESSING DOWNLINK TELEMETRY VECTOR FIELDS...")
        print(f"   >> Exit Stream Acceleration Impulse: {result['thrust_delivered']:.2f} uN")
        print(f"   >> Structural Core Thermal Sensor:    {result['temperature']:.1f} °C")
        
        if result["incidents_logged"]:
            for error in result["incidents_logged"]:
                print(f"   {error}")
        else:
            print("   ✅ Downlink Confirmed: Subsystems processing metrics smoothly inside nominal envelopes.")

        # FIX: Explicit Choice Array Checks resolve empty token code parsing failures completely
        if current_cycle == 1:
            if choice == 2 and result["thrust_delivered"] > 0:
                print("   [ACTION RESULT] High-thrust avoidance successful. Swept the zone and salvaged 2 scrap modules!")
                scrap += 2
            else:
                print("   💥 SHARD STRIKE: Avoidance failed or thrusters choked. Shrapnel shredded core thruster lines.")
                systems_health["propulsion"] = max(0, systems_health["propulsion"] - 45)

        elif current_cycle == 2:
            if choice == 4:
                print("   [ACTION RESULT] Command approved. Dormant profile successfully mitigated shadow thermal loads. Extracted 1 scrap casing.")
                scrap += 1
            elif result["temperature"] < 0:
                print("   ❄️ CRYSTALLIZATION STRAIN: Core chill caused microscopic frame stress fissures.")

        elif current_cycle == 3:
            if choice in [1, 2] and result["thrust_delivered"] > 0:
                print("   [ACTION RESULT] Boost sequence stabilized altitude against atmospheric friction.")
            else:
                print("   📉 APOGEE LOSS: Drag friction over-loaded structure, burning out avionics links.")
                systems_health["electronics"] = max(0, systems_health["electronics"] - 50)

        elif current_cycle == 4:
            if choice in [1, 2] and result["thrust_delivered"] > 0:
                print("   [ACTION RESULT] Capture arrays locked. Successfully ripped 3 high-grade salvage scraps from the dead hulk!")
                scrap += 3
            else:
                print("   [ACTION RESULT] Spacecraft drifted past the orbital marker. Salvage opportunity missed.")

        elif current_cycle == 5:
            if choice == 4:
                print("   [ACTION RESULT] Masterstroke. Cold shutdown completely insulated circuit arrays from ionization arcs.")
            else:
                print("   ⚡ SURGE INDUCTION: High-energy flare induction overloaded processing gates.")
                systems_health["electronics"] = max(0, systems_health["electronics"] - 45)

        # Re-check component life status after events before opening repair panel
        if any(h <= 0 for h in systems_health.values()):
            completed_mission = False
            break

        # Open Repair Interface Phase if inventory rules permit
        if scrap > 0 and current_cycle < total_cycles:
            systems_health, scrap = run_repair_phase(systems_health, scrap)

        if current_cycle == total_cycles and all(h > 0 for h in systems_health.values()):
            completed_mission = True

        current_cycle += 1
        if current_cycle <= total_cycles:
            print("\nInstruction vector completed. Press Enter to sync clock registers and enter next sector...")
            input()

    # Launch Scoreboard Engine
    print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission)

if __name__ == "__main__":
    play_orbital_command()
