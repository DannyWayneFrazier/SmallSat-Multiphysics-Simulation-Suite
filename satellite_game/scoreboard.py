"""
PART 4: SCOREBOARD EVALUATION
Assigns formal player rankings and final telemetry outputs.
"""

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
        print(f" 🛠️ CORES RESIDUAL HEALTH: {health_sum} (+{health_sum} pts)")
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
    print("====================================================================")
