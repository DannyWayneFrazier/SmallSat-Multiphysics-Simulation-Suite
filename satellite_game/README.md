# 🛰️ Orbital Command v4.5

A modular text-based orbital mechanics simulation and strategy game built in Python. Manage your ship's energy, propulsion, and thermals to complete your orbital tracking profile.

---

## 🎮 How to Run and Play

1. **Download the full project repository** as a ZIP file and extract it on your computer.
2. **Open your Terminal (Mac/Linux) or Command Prompt (Windows).**
3. **Use the `cd` command** to navigate to the main outside folder (where `run.py` is located).
   * *For example:* `cd Desktop/orbital-project`
4. **Run the game** by typing this command:
   ```bash
   python run.py
   ```

---

## 📋 Mission Briefing & Mechanics

Your ultimate goal is to stabilize your satellite's orbit by delivering a total of **500.00 uN of thrust**. If your ship takes catastrophic damage or falls behind, the mission fails.

### 📊 Understanding Telemetry (The Dashboard)
* **Target Thrust Remaining:** Starts at 500.00 uN. You win when this hits 0.00 uN.
* **Environment Gravity Drag Decay:** Cosmic friction pushes your satellite backward every single turn. This value increases dynamically as the run progresses!
* **Fuel & Battery:** Your two active fuel gauges. Running out of battery results in an immediate cold-start blackout.
* **Scrap Metal (🔧):** Gathered randomly from debris fields. Used to patch up structural hull damage.
* **Systems Health (Prop / Therm / Elec):** If *any* of these three system matrices drop to **0%**, your satellite is permanently destroyed.

---

## 🚀 Spacecraft Classes

Before launching, choose a chassis profile that matches your tactical survival style:

1. **Interceptor (High Thrust Efficiency)**
   * *Stats:* 50g Fuel | 80W Max Battery | 120% Propulsion Starting Health.
   * *Trait:* High engine efficiency, but drawing maximum current carries a higher risk of critical damage.
2. **Dreadnought (Heavy Armor)**
   * *Stats:* 85g Fuel | 100W Max Battery | 3 Starting Scrap.
   * *Trait:* Immune to cascading subsystem failures and environmental structural anomalies.
3. **Solar Probe (Advanced Energy Grid)**
   * *Stats:* 40g Fuel | 150W Max Battery | 120% Electronics Starting Health.
   * *Trait:* Captures solar arrays cleanly. Receives **double battery regeneration** when idling on standby core loops.

---

## 🛠️ Command Actions

Every turn, you must issue one of five baseline operational parameters:

1. **🚀 FEEP Micro-Thrust [-1.5g Fuel | -15W Battery]:** Delivers minor thrust progress. *Warning: Safe, but the low output can be completely swallowed by environmental drag decay!*
2. **🔥 High-Tension Burn [-12.0g Fuel | -45W Battery]:** Delivers massive, drag-shattering thrust. *Warning: Dangerous voltage loads carry a severe risk of dielectric arcing and physical component wear.*
3. **🌡️ Active Heating [-30W Battery]:** Pumps power into structural heat sinks to stabilize thermal systems against deep-space cold snaps.
4. **🔋 Recharge Array [+25W Battery]:** Deploys solar grids for high current intake. This requires a sub-zero cooling cycle which lowers your Thermal health.
5. **🛰️ Standby Core Loop [+12W Battery]:** Places primary computational systems into an idle state for basic balance baseline power cycles.

---

## ⚙️ Gameplay Features

* **Dynamic Environment Shifts:** Space is unpredictable. Your satellite will periodically warp into unique hazard sectors like the *Nebula Core* or *Asteroid Belt*.
* **Infinite Difficulty Scaling:** Background cosmic hazards, orbital radiation matrix loops, and environmental drag increase dynamically every 3 turns.
* **Component Recovery & Repairs:** Prompt the Maintenance Bay at the end of a successful turn to convert floating scrap metal into immediate structural system repairs.
* **Active Session Persistence:** Type `save` during any turn selection to back up your telemetry state matrices, or `load` at boot to resume a previous run.
* **Modular Codebase:** Clean, split architecture utilizing dedicated physics engines, visual telemetry panels, and state tracking files.
