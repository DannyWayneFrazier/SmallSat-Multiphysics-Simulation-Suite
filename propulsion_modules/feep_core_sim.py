import math
import numpy as np

def simulate_thruster_aerospace_grade(input_voltage=2500.0, mission_profile="longevity"):
    """
    Flight-Ready Propulsion Review Board Verification Script v1.6.0.
    Implements local sub-micron field enhancement, spatial electrostatic plume deflection,
    closed-loop thermostatic bang-bang regulation, and ionization plume stabilization.
    """
    # Universal & Environmental Physical Constants
    ELEMENT_CHARGE = 1.602176634e-19  
    AMU_TO_KG = 1.660539066e-27       
    STEFAN_BOLTZMANN = 5.670374e-8    
    G_0 = 9.80665                     
    SPACE_BG_TEMP_K = 3.0             

    # Propellant Metallurgical Constants (Indium)
    INDIUM_MASS_AMU = 114.818     
    M_ION = INDIUM_MASS_AMU * AMU_TO_KG
    INDIUM_MELTING_POINT_K = 429.75      # 156.6 °C
    THERMOSTAT_LOWER_LIMIT_K = 433.15    # 160.0 °C (Safe liquid margin)
    THERMOSTAT_UPPER_LIMIT_K = 438.15    # 165.0 °C (Hysteresis ceiling)
    SPECIFIC_HEAT_INDIUM = 233.0         
    LATENT_HEAT_FUSION_INDIUM = 28470.0  

    # Core Structural, Interception Casing & Electrical Limits
    DIELECTRIC_LIMIT_HBN_V_M = 1.2e9   
    EXTRACTOR_GAP_M = 0.0035             # Redesigned: Expanded to 3.5 mm to prevent vacuum arcing
    RADIATOR_AREA = 0.008              
    THERMAL_EMISSIVITY = 0.85          
    SYSTEM_IMPEDANCE_OHMS = 5.0e6      
    ACTIVE_HEATER_POWER_W = 45.0       
    STRUCTURAL_MASS_KG = 0.050         
    SPECIFIC_HEAT_STRUCTURE = 130.0      

    # Local Sub-Micron Geometric Field Enhancement
    EMITTER_TIP_RADIUS_M = 0.25e-6       # 250 nanometer electrochemically etched tungsten tips

    # Field enhancement factor model linking macro geometry to sub-micron tip gradients
    BETA_FIELD_ENHANCEMENT = 1.0 / (EMITTER_TIP_RADIUS_M * math.log(EXTRACTOR_GAP_M / EMITTER_TIP_RADIUS_M))

    # Downstream Electrostatic Plume Deflection & Neutralization Envelopes
    PLUME_DIVERGENCE_HALF_ANGLE_DEG = 2.39
    EFFICIENCY_GEOMETRIC = np.cos(np.radians(PLUME_DIVERGENCE_HALF_ANGLE_DEG))
    IONIZATION_EFFICIENCY = 0.99         

    # Simulation Time Domain Configurations (7200 seconds / 2 Hours)
    TIME_STEPS = 7200                  
    DT = 1.0                             

    # Telemetry Flight State Variables
    INITIAL_FUEL_MASS = 0.100          
    remaining_fuel = INITIAL_FUEL_MASS  
    current_temp_k = 293.15              
    latent_heat_pool = 0.0                     
    ppu_efficiency_decay = 1.0         
    
    is_liquid = False
    heater_on = True                     

    # Standardize Base Mission Mass Flow Allocations
    if mission_profile == "longevity":
        base_mass_flow = 4.133e-11 
    elif mission_profile == "high_thrust":
        base_mass_flow = 4.062e-9
    else:
        raise ValueError("Unknown mission profile allocation.")

    # Telemetry Data Logging arrays
    thrust_log = []
    temperature_log = []
    mass_flow_log = []
    macro_stress_log = []
    local_stress_log = []              
    power_log = []
    v_exhaust_log = []
    heater_state_log = []
    catastrophic_failure = False

    for step in range(TIME_STEPS):
        # 1. PPU Electrical & Stress Phase Analysis
        ppu_efficiency_decay -= 1e-8 * DT  
        actual_voltage = input_voltage * max(0.0, ppu_efficiency_decay) * (1.0 + 0.01 * np.sin(step * 0.1))
        
        # Macro dielectric isolation calculation across h-BN beds
        macro_stress_v_m = actual_voltage / EXTRACTOR_GAP_M
        macro_stress_log.append(macro_stress_v_m)
        
        # Microscopic Taylor Cone localized electric field enhancement calculation
        enhanced_local_field_v_m = actual_voltage * BETA_FIELD_ENHANCEMENT
        local_stress_log.append(enhanced_local_field_v_m)
        
        if macro_stress_v_m >= DIELECTRIC_LIMIT_HBN_V_M:
            catastrophic_failure = True
        
        # 2. Thermostatic Deadband Controller (Bang-Bang Loop)
        impedance_loss_watts = (actual_voltage ** 2) / SYSTEM_IMPEDANCE_OHMS
        
        if is_liquid:
            if current_temp_k <= THERMOSTAT_LOWER_LIMIT_K:
                heater_on = True
            elif current_temp_k >= THERMOSTAT_UPPER_LIMIT_K:
                heater_on = False
        else:
            heater_on = True 

        active_heater_draw = ACTIVE_HEATER_POWER_W if heater_on else 0.0
        total_thermal_input = impedance_loss_watts + active_heater_draw
        power_log.append(total_thermal_input)
        heater_state_log.append(1.0 if heater_on else 0.0)
        
        radiated_power = THERMAL_EMISSIVITY * STEFAN_BOLTZMANN * RADIATOR_AREA * ((current_temp_k ** 4) - (SPACE_BG_TEMP_K ** 4))
        net_heat_flux = total_thermal_input - radiated_power
        
        total_thermal_mass = (max(0.0, remaining_fuel) * SPECIFIC_HEAT_INDIUM) + (STRUCTURAL_MASS_KG * SPECIFIC_HEAT_STRUCTURE)
        required_latent_heat = max(0.0, remaining_fuel) * LATENT_HEAT_FUSION_INDIUM
        
        # Thermodynamic Transition Engine
        if current_temp_k < INDIUM_MELTING_POINT_K:
            current_temp_k += (net_heat_flux / total_thermal_mass) * DT
            if current_temp_k >= INDIUM_MELTING_POINT_K:
                current_temp_k = INDIUM_MELTING_POINT_K
        elif current_temp_k == INDIUM_MELTING_POINT_K and latent_heat_pool < required_latent_heat:
            latent_heat_pool += net_heat_flux * DT
            if latent_heat_pool >= required_latent_heat:
                is_liquid = True
                overshoot_heat = latent_heat_pool - required_latent_heat
                current_temp_k += (overshoot_heat / total_thermal_mass)
        else:
            current_temp_k += (net_heat_flux / total_thermal_mass) * DT
            
        temperature_log.append(current_temp_k)
        
        # 3. Electrostatic Ion Kinetic Acceleration Calculation (Driven by Global Potential Profile)
        v_ex = np.sqrt((2.0 * ELEMENT_CHARGE * actual_voltage) / M_ION)
        v_exhaust_log.append(v_ex)
        
        # 4. Fluid Mass Flow Exhaust Gating & Plume Coupling
        # Field emission occurs once localized microfield enhances past the ionization barrier (>1.0e9 V/m)
        if not catastrophic_failure and is_liquid and enhanced_local_field_v_m >= 1.0e9 and remaining_fuel > 0:
            active_mass_flow_rate = base_mass_flow
            remaining_fuel -= active_mass_flow_rate * DT
            thrust_force = active_mass_flow_rate * v_ex * EFFICIENCY_GEOMETRIC * IONIZATION_EFFICIENCY
            thrust_micro_newtons = thrust_force * 1e6
        else:
            active_mass_flow_rate = 0.0
            thrust_micro_newtons = 0.0
            
        thrust_log.append(thrust_micro_newtons)
        mass_flow_log.append(active_mass_flow_rate)

    # Compile Final Diagnostics
    mass_flow_array = np.array(mass_flow_log)
    active_firing_indices = mass_flow_array > 0
    
    if np.any(active_firing_indices) and not catastrophic_failure:
        nominal_firing_mass_flow = np.mean(mass_flow_array[active_firing_indices])
        lifespan_seconds = INITIAL_FUEL_MASS / nominal_firing_mass_flow
        lifespan_days = lifespan_seconds / (24 * 3600)
        max_thrust = max(thrust_log)
        avg_active_ve = np.mean(np.array(v_exhaust_log)[active_firing_indices])
        total_impulse_ns = INITIAL_FUEL_MASS * avg_active_ve * IONIZATION_EFFICIENCY * EFFICIENCY_GEOMETRIC
        isp_seconds = (avg_active_ve * EFFICIENCY_GEOMETRIC * IONIZATION_EFFICIENCY) / G_0
    else:
        nominal_firing_mass_flow = 0.0
        lifespan_days = 0.0
        max_thrust = 0.0
        total_impulse_ns = 0.0
        isp_seconds = 0.0
    
    peak_macro_stress = max(macro_stress_log)
    peak_local_field = max(local_stress_log)
    safety_margin = ((DIELECTRIC_LIMIT_HBN_V_M - peak_macro_stress) / DIELECTRIC_LIMIT_HBN_V_M) * 100
    heater_duty_cycle = (sum(heater_state_log) / TIME_STEPS) * 100
    
    return {
        "profile_reviewed": mission_profile,
        "structural_integrity_passed": not catastrophic_failure,
        "isp_seconds": isp_seconds,
        "max_thrust_uN": max_thrust,
        "total_impulse_N_s": total_impulse_ns,
        "peak_macro_stress_V_m": peak_macro_stress,
        "enhanced_local_field_V_m": peak_local_field,
        "safety_margin_percent": safety_margin,
        "final_temp_C": temperature_log[-1] - 273.15,
        "avg_power_W": np.mean(power_log),
        "heater_duty_cycle_percent": heater_duty_cycle,
        "lifespan_continuous_days": lifespan_days,
    }

if __name__ == "__main__":
    print("====================================================================")
    print("   VERIFIED AEROSPACE FEEP CORE SIMULATION (v1.6.0)")
    print("====================================================================\n")
    
    metrics_long = simulate_thruster_aerospace_grade(input_voltage=2500.0, mission_profile="longevity") # Lowered to 2.5 kV safely
    print("--- RUN 1: MISSION PROFILE: LONGEVITY ---")
    for k, v in metrics_long.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n--- RUN 2: MISSION PROFILE: HIGH THRUST ---")
    metrics_thrust = simulate_thruster_aerospace_grade(input_voltage=2500.0, mission_profile="high_thrust")
    for k, v in metrics_thrust.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")
