"""
PART 3: MAINTENANCE PROCEDURES
Handles internal engineering bay processes for component recovery.
"""

def run_repair_phase(systems_health, scrap_count, ship_class=""):
    """Handles internal engineering bay processes for component recovery."""
    updated_health = systems_health.copy()
    
    # Cap thresholds based on ship configurations
    prop_max = 120 if ship_class == "Interceptor" else 100
    elec_max = 120 if ship_class == "Solar Probe" else 100
    therm_max = 100

    while scrap_count > 0:
        if updated_health["propulsion"] >= prop_max and updated_health["thermal"] >= therm_max and updated_health["electronics"] >= elec_max:
            print("\n✨ All systems operating at maximum class capacity. Closing maintenance window.")
            break
            
        print(f"\n🔧 [MAINTENANCE BAY] Casing Scrap Available: {scrap_count} units")
        print(f"   🚀 Propulsion: {updated_health['propulsion']}%/{prop_max}% | 🛡️ Thermal: {updated_health['thermal']}%/{therm_max}% | ⚡ Electronics: {updated_health['electronics']}%/{elec_max}%")
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
                if updated_health["propulsion"] >= prop_max:
                    print("❌ Propulsion systems already maximized.")
                else:
                    updated_health["propulsion"] = min(prop_max, updated_health["propulsion"] + 25)
                    scrap_count -= 1
            elif fix_choice == 2:
                if updated_health["thermal"] >= therm_max:
                    print("❌ Thermal shield layers already operating at maximum capacity.")
                else:
                    updated_health["thermal"] = min(therm_max, updated_health["thermal"] + 25)
                    scrap_count -= 1
            elif fix_choice == 3:
                if updated_health["electronics"] >= elec_max:
                    print("❌ Electronics systems already maximized.")
                else:
                    updated_health["electronics"] = min(elec_max, updated_health["electronics"] + 25)
                    scrap_count -= 1
            else:
                print("❌ Invalid choice. Please select 1-4.")
        except ValueError:
            print("❌ Input verification failed. Numeric parameter required.")
            
    return updated_health, scrap_count
