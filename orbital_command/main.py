"""
PART 7: SYSTEM RESOLUTION ENGINE & MAIN EXECUTABLE
Links peripheral dependencies together into a unified gameplay simulation framework.
"""
import random
import engine_core as core
import physics_sim as physics
import maintenance as maint
import scoreboard as score_eval
import save_manager as storage
import dashboard as gui

def play_orbital_command():
    """Main sequence game initialization and sector turn navigation."""
    print("==================================================")
    print("        🛰️ WELCOME TO ORBITAL COMMAND v4.5 🛰️      ")
    print("==================================================")
    
    print("\nCHOOSE YOUR SPACECRAFT CLASS:")
    print("1. 🚀 INTERCEPTOR (High Thrust Efficiency | 50g Fuel | 80W Max Battery)")
    print("   *Special: Starts with 120% Propulsion Health, but burning fuel is riskier.")
    print("2. 🛡️ DREADNOUGHT (Heavy Armor | 85g Fuel | 100W Max Battery | 3 Starting Scrap)")
    print("   *Special: Immune to cascading subsystem failures.")
    print("3. 🛰️ SOLAR PROBE (Advanced Energy Grid | 40g Fuel | 150W Max Battery)")
    print("   *Special: Electronics start at 120% Health. Gains double battery on standby.")
    
    jump_to_loop = False
    skip_decay_once = False

    class_choice = input("\nEnter class selection (1-3) [Default 2] or type 'load': ").strip().lower()
    
    if class_choice == 'load':
        save_data = storage.read_save_state()
        if save_data:
            ship_class = save_data["ship_class"]
            fuel_g = save_data["fuel_g"]
            battery_w = save_data["battery_w"]
            max_battery = save_data["max_battery"]
            scrap = save_data["scrap"]
            systems_health = save_data["systems_health"]
            total_thrust_delivered = save_data["total_thrust_delivered"]
            turn = save_data["turn"]
            current_sector = save_data["current_sector"]
            sector_turns_left = save_data["sector_turns_left"]
            print(f"\n💾 LOAD SUCCESSFUL: Resuming [{ship_class.upper()} CLASS] run at Turn {turn}!")
            jump_to_loop = True
        else:
            print("\n❌ LOAD ERROR: Save file invalid, corrupted, or missing! Initializing default Dreadnought.")
            class_choice = "2"

    if not jump_to_loop:
        selected_cfg = core.SHIP_CLASSES.get(class_choice, core.SHIP_CLASSES["2"])
        ship_class = selected_cfg["name"]
        fuel_g = selected_cfg["fuel"]
        battery_w = selected_cfg["battery"]
        max_battery = selected_cfg["max_battery"]
        scrap = selected_cfg["scrap"]
        systems_health = selected_cfg["health"].copy()
        
        print(f"\n✅ Flight profile loaded: [{ship_class.upper()} CLASS] initialized.")
        total_thrust_delivered = 0.0
        turn = 1
        current_sector = random.choice(core.SECTORS_POOL)
        sector_turns_left = random.randint(6, 10)

    # Core Execution Loop
    while total_thrust_delivered < core.TARGET_THRUST:
        if sector_turns_left <= 0:
            next_options = [s for s in core.SECTORS_POOL if s != current_sector]
            current_sector = random.choice(next_options)
            sector_turns_left = random.randint(6, 10)
            print(f"\n🚨 WARP SPACE ALERT: Satellite transitioned into the [{current_sector.upper()}] environment!")
        
        # Calculate sector modifiers and drag decay
        total_thrust_delivered, drag_loss, salvage_rate_modifier, battery_gen_mod = gui.apply_environmental_rules(
            current_sector, total_thrust_delivered, turn, skip_decay_once
        )
        skip_decay_once = False 

        # Render panel interfaces
        gui.show_telemetry_panel(
            turn, ship_class, current_sector, sector_turns_left, drag_loss, 
            core.TARGET_THRUST, total_thrust_delivered, fuel_g, battery_w, max_battery, scrap, systems_health
        )

        if current_sector == "Asteroid Belt" and random.random() < 0.20:
            systems_health["thermal"] = max(0, systems_health["thermal"] - 15)
            print("☄️ METEOROID IMPACT: Small dust grains scraped across thermal hulls! (-15% Thermal Health)")

        # Proactive system destruction check
        if any(health <= 0 for health in systems_health.values()):
            score_eval.print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=False)
            return

        print("\nSelect Next Sector Action:")
        print("  1. 🚀 FEEP Micro-Thrust  [-1.5g Fuel | -15W Battery | +Low Thrust]")
        print("  2. 🔥 High-Tension Burn  [-12.0g Fuel | -45W Battery | +High Thrust | Danger: Arcing]")
        print("  3. 🌡️ Active Heating    [-30W Battery | Warm internal grid system]")
        print("  4. 🔋 Recharge Array     [+25W Battery | Sub-zero cool state cycle]")
        print("  5. 🛰️ Standby Core Loop  [+12W Battery | Base balance baseline cycle]")
        print("💡 Alternatively, type 'save' to backup progress or 'load' to resume a save state.")

        user_action = input("Enter action (1-5 or save/load): ").strip().lower()

        if user_action == "save":
            state = {
                "ship_class": ship_class, "fuel_g": fuel_g, "battery_w": battery_w,
                "max_battery": max_battery, "scrap": scrap, "systems_health": systems_health,
                "total_thrust_delivered": total_thrust_delivered, "turn": turn,
                "current_sector": current_sector, "sector_turns_left": sector_turns_left
            }
            storage.write_save_state(state)
            skip_decay_once = True
            continue  
            
        elif user_action == "load":
            save_data = storage.read_save_state()
            if save_data:
                ship_class = save_data["ship_class"]
                fuel_g = save_data["fuel_g"]
                battery_w = save_data["battery_w"]
                max_battery = save_data["max_battery"]
                scrap = save_data["scrap"]
                systems_health = save_data["systems_health"]
                total_thrust_delivered = save_data["total_thrust_delivered"]
                turn = save_data["turn"]
                current_sector = save_data["current_sector"]
                sector_turns_left = save_data["sector_turns_left"]
                print(f"\n💾 LOAD SUCCESSFUL: Reverted telemetry to Turn {turn} state matrices!")
                skip_decay_once = True
            else:
                print("\n❌ LOCAL ARCHIVE RECOVERY FAILURE: File missing or corrupt.")
            continue

        # Command interpreter validation to patch the environmental cheat glitch
        if user_action not in ["1", "2", "3", "4", "5", ""]:
            print("❌ Invalid command parameter input! Forcing system baseline safety cycle.")
            action = 5
        else:
            try:
                action = int(user_action) if user_action else 5
                if action < 1 or action > 5:
                    action = 5
            except ValueError:
                action = 5

        # Execute physics simulation
        result = physics.run_physics_turn(action, fuel_g, battery_w, systems_health, turn, ship_class)
        
        if ship_class == "Solar Probe" and action == 5:
            print("🔋 SOLAR PROBE BONUS: Solar panels optimized! Charging rate doubled.")
            result["battery_delta"] = 24.0 * battery_gen_mod
        elif result["battery_delta"] > 0:
            result["battery_delta"] *= battery_gen_mod
        
        # Apply physics differentials
        fuel_g = max(0.0, fuel_g - result["fuel_burned"])
        battery_w = min(max_battery, max(0.0, battery_w + result["battery_delta"]))
        total_thrust_delivered += result["thrust_delivered"]
        systems_health = result["updated_health"]
        
        if ship_class == "Interceptor" and "💥 DIELECTRIC ARCING: 3.5 kV tension breached h-BN beds! Propulsion damaged." in result["incidents_logged"]:
            print("💥 INTERCEPTOR penalty: Fragile speed systems took extra structural damage!")
            systems_health["propulsion"] = max(0, systems_health["propulsion"] - 15)

        if result["incidents_logged"]:
            print("\n⚠️ TURN LOG WARNINGS:")
            for incident in result["incidents_logged"]:
                print(f"  {incident}")
        else:
            print("\n✨ Sector navigation smooth. No anomalies recorded.")

        # Main terminal crash verification check
        if any(health <= 0 for health in systems_health.values()):
            score_eval.print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=False)
            return

        # Handle salvage mechanics
        if random.random() < salvage_rate_modifier:
            found_scrap = random.randint(1, 2)
            print(f"📦 ORBITAL SALVAGE: Found {found_scrap} unit(s) of usable casing scrap metal!")
            scrap += found_scrap

        # Trigger maintenance options
        if scrap > 0:
            prompt_repair = input(f"\n🔧 Scrap available ({scrap} units). Open maintenance bay? (y/n): ").strip().lower()
            if prompt_repair == 'y':
                systems_health, scrap = maint.run_repair_phase(systems_health, scrap, ship_class)

        # Softlock verification check
        if fuel_g < 1.5 and total_thrust_delivered < core.TARGET_THRUST:
            score_eval.print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=False, softlocked=True)
            return

        sector_turns_left -= 1
        turn += 1

    score_eval.print_scoreboard(fuel_g, battery_w, systems_health, scrap, completed_mission=True)

if __name__ == "__main__":
    play_orbital_command()
