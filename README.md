# Unified SmallSat Multiphysics Simulation Suite & Orbital Survival Engine (v4.0.0)

## 📢 Core Project Origin & Technical Disclosure
**This repository serves as a concrete demonstration of high-level system logic architecture, multi-variable code synchronization, and advanced AI-assisted technical debugging.**

*   **Theoretical Framework:** This software provides 1D macro-level numerical approximations of standard, known electric propulsion, quantum tunneling, and material thermodynamic physics. It is intended purely as a software system design demonstration.
*   **Intellectual Property:** The mathematical equations and physical principles simulated herein (such as liquid Indium extraction boundaries and WKB tunneling approximations) are well-documented public knowledge in aerospace literature. This project does not claim to hold proprietary hardware inventions or commercial aerospace patents.
*   **Engineering Process:** The value of this suite lies in the **iterative prompt orchestration process**. The codebase was generated, audited, and hardened across multiple AI models to actively catch, troubleshoot, and eliminate hidden algorithmic flaws (such as inverted voltage feedback loops, fluid relaxation time lags, and one-way thermodynamic calculation traps).

---

## 🎮 Interactive Core: Orbital Command Survival Game (`satellite_game.py`)
To demonstrate the practical integration of these separate physics matrices, the root directory features a fully interactive, text-based tactical orbital management game. 

The game loop feeds the player's real-time choices directly into the underlying simulation scripts, modeling component degradation alarms, structural thermal thresholds, and dynamic power storage limitations tied directly to system health.

---

## 📂 The Modular Propulsion Suite (`/propulsion_modules`)

### 🛰️ 1. FEEP Core Simulator (`feep_core_sim.py`)
Models an advanced Field Emission Electric Propulsion thruster utilizing liquid Indium propellant flowing over sub-micron, electrochemically etched tungsten tips. Tracks closed-loop thermostatic hysteresis loops alongside macro vs. micro-dielectric insulation stress across hexagonal Boron Nitride (h-BN) beds.

### 💨 2. Self-Ballasted CNT Neutralizer (`cnt_neutralizer_sim.py`)
Simulates an active electron field-emission gun array protected by an Atomic Layer Deposition (ALD) Alumina thin-film barrier. Accurately tracks WKB quantum tunneling transmission coefficients through a field-dependent triangular potential barrier, balanced against a global current-limiting ballast safety network.

### 💧 3. AC Colloid Thruster Matrix (`colloid_thruster_sim.py`)
Computes low-interference electrostatic microthrust profiles. Features explicit propellant mass-flow phase-splitting (segregating atomic ions from liquid droplets) and calculates a custom 0.85 ms hydrodynamic relaxation delay to model real-world Taylor Cone fluid meniscus deformation lag.

### 🛡️ 4. Honeycomb Solid-Solid Phase Change Shield (`thermal_shield_sim.py`)
A robust transient thermal management engine modeling a Solid-Solid Phase Change Material (SSPCM) cast inside an aluminum honeycomb matrix. Features a fully bidirectional latent heat plateau handling routine (tracking crystalline melting vs. eclipse freezing) and monitors interfacial shear stress primered with silane coupling layers.

---

## 🛠️ Verification & Software Specifications
*   **Language Environment:** Python 3.x / NumPy
*   **Architecture Phase:** Verified TRL 3 Analytical Model (Analytical Proof-of-Concept Frozen)
*   **License:** MIT Open-Source
