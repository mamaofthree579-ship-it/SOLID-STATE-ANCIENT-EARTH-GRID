import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# THE SOLID-STATE EARTH GRID PHYSICS SIMULATION ENGINE
# =========================================================
# Core Thermodynamic and Solid-State Physical Constants
RHO_WATER = 1000.0
RHO_AIR = 1.2
BULK_MODULUS_WATER = 2.2e9
C_AIR = 348.0
ST_NUM = 0.21
DENSITY_GRANITE = 2700.0
DENSITY_LIMESTONE = 2500.0
VEL_LIMESTONE = 2500.0
VEL_GRANITE = 5000.0
D_33_QUARTZ = 2.3e-12

def simulate_giza_piezocore(mass_tonnes, height_m, quartz_ratio=0.15):
    mass_kg = mass_tonnes * 1000.0
    area_base = mass_kg / (DENSITY_GRANITE * height_m)
    static_load_pa = (mass_kg * 9.81) / area_base
    f_natural = VEL_GRANITE / (2.0 * height_m)
    z1 = DENSITY_GRANITE * VEL_LIMESTONE
    z2 = DENSITY_GRANITE * VEL_GRANITE
    reflection_coeff = (z2 - z1) / (z2 + z1)
    
    t = np.linspace(0, 2, 500)
    seismic_ripple = 5000.0 * np.sin(2.0 * np.pi * 1.5 * t)
    total_stress = static_load_pa + seismic_ripple
    charge_density = D_33_QUARTZ * total_stress * quartz_ratio
    return t, charge_density, static_load_pa, f_natural, reflection_coeff

def simulate_quetzalcoatl_hull(velocity_knots, articulation_deg):
    v_ms = velocity_knots * 0.51444
    l_nominal = 15.0
    l_effective = l_nominal * np.cos(np.radians(articulation_deg))
    froude_number = v_ms / np.sqrt(9.81 * l_effective)
    base_cd = 0.05
    wave_cd = 0.25 * (froude_number ** 4)
    if articulation_deg > 0:
        wave_cd *= np.clip(1.0 - (articulation_deg / 90.0), 0.5, 1.0)
    total_drag = 0.5 * RHO_WATER * (v_ms**2) * l_effective * (base_cd + wave_cd)
    return l_effective, froude_number, total_drag

def simulate_tikal_ram(catchment_area, rainfall_mm_hr, height_m):
    v_rain = (rainfall_mm_hr / 1000.0) / 3600.0
    q_influx = catchment_area * v_rain
    mass_pyramid = (1.0/3.0) * catchment_area * height_m * DENSITY_LIMESTONE
    static_p = (mass_pyramid * 9.81) / catchment_area
    v_fluid = q_influx / 0.5
    c_wave = np.sqrt(BULK_MODULUS_WATER / RHO_WATER)
    delta_p_hammer = RHO_WATER * c_wave * v_fluid
    total_p = static_p + delta_p_hammer
    lift_m = total_p / (RHO_WATER * 9.81)
    return mass_pyramid, delta_p_hammer, lift_m

def simulate_rapa_nui_road(statue_mass_kg, road_radius, tilt_deg):
    theta_rad = np.radians(tilt_deg)
    h_com = 1.8
    pe_max = statue_mass_kg * 9.81 * h_com * (1.0 - np.cos(theta_rad))
    restoring_force = statue_mass_kg * 9.81 * np.sin(np.arctan(1.0 / road_radius))
    restoring_torque = restoring_force * h_com
    critical_tilt = np.degrees(np.arctan(0.6 / h_com))
    return pe_max, restoring_torque, critical_tilt

def simulate_giza_shafts(aperture_d, wind_speed, cavity_vol, shaft_len):
    f_vortex = (ST_NUM * wind_speed) / aperture_d
    area_shaft = 0.045
    f_helmholtz = (C_AIR / (2.0 * np.pi)) * np.sqrt(area_shaft / (cavity_vol * shaft_len))
    return f_vortex, f_helmholtz

def simulate_puma_punku_h_block(seismic_amplitude, frequency_hz, slot_depth_m=0.15):
    velocity_andesite = 6000.0
    wavelength = velocity_andesite / max(frequency_hz, 1.0)
    phase_shift_rad = (2.0 * np.pi * slot_depth_m) / wavelength
    cancellation_efficiency = np.abs(np.sin(phase_shift_rad))
    attenuation_db = -20.0 * np.log10(max(1.0 - cancellation_efficiency, 1e-2))
    return attenuation_db

# ---------------------------------------------------------
# Dynamic Chart Range Generators
# ---------------------------------------------------------
def generate_tikal_lift_curve(catchment_area, height_m, max_rain=150):
    rain_range = np.linspace(10, max_rain, 100)
    lift_depths = []
    for r in rain_range:
        _, _, lift_m = simulate_tikal_ram(catchment_area, r, height_m)
        lift_depths.append(lift_m)
    return rain_range, np.array(lift_depths)

def generate_quetzalcoatl_drag_curve(velocity_knots):
    angles = np.linspace(0, 45, 100)
    drag_forces = []
    for a in angles:
        _, _, drag = simulate_quetzalcoatl_hull(velocity_knots, a)
        drag_forces.append(drag)
    return angles, np.array(drag_forces)

def generate_puma_punku_curve(slot_depth):
    freq_range = np.linspace(10, 500, 150)
    attenuations = []
    for f in freq_range:
        att = simulate_puma_punku_h_block(seismic_amplitude=1.0, frequency_hz=f, slot_depth_m=slot_depth)
        attenuations.append(att)
    return freq_range, np.array(attenuations)

def calculate_richter_pga_stress(magnitude, distance_km):
    pga_g = (10**(0.76 * magnitude - np.log10(distance_km) - 0.0025 * distance_km)) / 9.81
    pga_g = np.clip(pga_g, 0.01, 2.5)
    raw_stress_pa = 2800.0 * (pga_g * 9.81) * 3.5
    return pga_g, raw_stress_pa
# ---------------------------------------------------------
# Streamlit Layout User Interface Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="SS-AEGIC Simulator", layout="wide")

st.title("🌐 Solid-State Ancient Earth-Grid Simulation Core (SS-AEGIC)")
st.markdown("""
This open-source dashboard strips away historical paradigms of primitive superstition and models ancient monumental engineering through the lens of **solid-state physics, geodetics, and trans-medium fluid dynamics**.
""")

# Sidebar Navigation Panel
node = st.sidebar.selectbox("Select Engineering Node", [
    "Overview & Universal Lexicon",
    "Giza Resonator & Tuned Shafts (Egypt)",
    "Quetzalcoatl Trans-Medium Vessel",
    "Tikal Macrofluidic Ram Pump (Maya)",
    "Rapa Nui Grid & Concave Roadways",
    "Puma Punku Acoustic Filter Array (Bolivia)"
])

# Node 1: Overview & Universal Lexicon
if node == "Overview & Universal Lexicon":
    st.header("📋 The Universal Engineering Lexicon")
    st.table([
        {"Traditional Archeology Label": "God / Deity", "Solid-State Engineering Equivalent": "Fundamental Field Force (Gravity, EM, Tension)"},
        {"Traditional Archeology Label": "Sacred Statue / Idol", "Solid-State Engineering Equivalent": "Tuned Mechanical Transducer / Resonator"},
        {"Traditional Archeology Label": "Temple / Sanctuary", "Solid-State Engineering Equivalent": "Enclosed Capacitive Power Terminal Hub"},
        {"Traditional Archeology Label": "Sacred Holy Road", "Solid-State Engineering Equivalent": "Energy Bus Line / High-Mass Waveguide"},
        {"Traditional Archeology Label": "Ritual / Chant / Legend", "Solid-State Engineering Equivalent": "System Frequency Calibration / Operational Manual"}
    ])
    st.info("💡 Select an engineering node in the sidebar to begin loading specialized fluid and wave mechanics simulators.")

# Node 2: Giza Resonator & Tuned Shafts
elif node == "Giza Resonator & Tuned Shafts (Egypt)":
    st.header("📐 Giza Tectonic Waveguide & Acoustic Interferometer")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Control Parameters")
        mass = st.slider("Granite Core Mass Loading (Tonnes)", 10000, 100000, 60000, step=5000)
        height = st.slider("Core Vertical Matrix Height (Meters)", 3.0, 15.0, 5.8, step=0.1)
        quartz = st.slider("Quartz Crystalline Ratio (SiO2 %)", 0.05, 0.30, 0.15, step=0.01)
        wind = st.slider("External Air-Shaft Wind Speed (m/s)", 2.0, 25.0, 12.0, step=0.5)
        
    with col2:
        t, charge, static_p, f_nat, ref_coeff = simulate_giza_piezocore(mass, height, quartz)
        f_vort, f_helm = simulate_giza_shafts(0.2, wind, 250.0, 60.0)
        st.metric("Tuned Core Frequency", f"{f_nat:.2f} Hz")
        st.metric("Static Gravitational Compression Load", f"{static_p/1e3:.2f} kPa")
        st.metric("Heterojunction Energy Capture Ratio", f"{ref_coeff*100:.1f}%")
        st.metric("Helmholtz Air-Cavity Resonance", f"{f_helm:.2f} Hz")
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, charge * 1e12, color='#E67E22', linewidth=2)
        ax.set_title("Piezoelectric Polarization Field Output over Time")
        ax.set_xlabel("Seismic Period Window (Seconds)")
        ax.set_ylabel("Charge Density (pC/m²)")
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

# Node 3: Quetzalcoatl Trans-Medium Vessel
elif node == "Quetzalcoatl Trans-Medium Vessel":
    st.header("🛶 Quetzalcoatl Trans-Medium Wave Mechanics")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Velocity & Articulation Anchors")
        knots = st.slider("Vessel Velocity (Knots)", 2, 25, 12)
        tilt = st.slider("Serpentine Hull Articulation Angle (Degrees)", 0.0, 45.0, 22.5, step=2.5)
        
    with col2:
        l_eff, fr, drag = simulate_quetzalcoatl_hull(knots, tilt)
        st.metric("Effective Waterline Footprint", f"{l_eff:.2f} meters")
        st.metric("Calculated Froude Index (Fr)", f"{fr:.3f}")
        st.metric("Net Dynamic Wave Resistance", f"{drag:.2f} Newtons")
        
        angles_x, drag_y = generate_quetzalcoatl_drag_curve(knots)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(angles_x, drag_y / 1e3, color='#2980B9', linewidth=2.5)
        ax.axvline(x=tilt, color='#E67E22', linestyle='--')
        ax.set_title("Wave Drag Attenuation via Serpentine Geometry Adjustments")
        ax.set_xlabel("Hull Articulation Shift (Degrees)")
        ax.set_ylabel("Total Dynamic Resistance (Kilo-Newtons)")
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

# Node 4: Tikal Macrofluidic Ram Pump
elif node == "Tikal Macrofluidic Ram Pump (Maya)":
    st.header("⚡ Tikal Macrofluidic Mass-Actuated Ram Pump")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Control Parameters")
        area = st.slider("Pluvial Catchment Basin Area (m²)", 500, 5000, 2500, step=250)
        rain = st.slider("Monsoonal Rainfall Rate (mm/hour)", 10, 150, 75, step=5)
        p_height = st.slider("Pyramid Mass Actuator Height (Meters)", 10, 80, 47)
        
    with col2:
        mass, hammer, lift = simulate_tikal_ram(area, rain, p_height)
        st.metric("Total Pyramid Structural Mass Action", f"{mass/1e6:.3f} Megatonnes")
        st.metric("Transient Water-Hammer Shockwave Pressure", f"{hammer/1e6:.2f} MPa")
        st.metric("Hydro-Pneumatic Fluid Elevation Lift", f"{lift:.2f} meters")
        
        rain_x, lift_y = generate_tikal_lift_curve(area, p_height, max_rain=150)
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(rain_x, lift_y, color='#1ABC9C', linewidth=2.5)
        ax.axvline(x=rain, color='#E74C3C', linestyle='--')
        ax.set_title("Fluid Head Lift Vector vs. Monsoonal Intensity")
        ax.set_xlabel("Rainfall Rate (mm / hour)")
        ax.set_ylabel("Maximum Vertical Water Lift (Meters)")
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

# Node 5: Rapa Nui Grid & Concave Roadways
elif node == "Rapa Nui Grid & Concave Roadways":
    st.header("🗿 Rapa Nui Groundwater Sieve & Road Waveguides")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("System Control Parameters")
        s_mass = st.slider("Moai Transducer Column Mass (kg)", 5000, 80000, 15000, step=2000)
        radius = st.slider("Roadway Concave Geometry Radius (meters)", 1.5, 10.0, 3.5, step=0.5)
        tilt = st.slider("Dynamic Sway Walking Tilt Angle (Degrees)", 1.0, 15.0, 6.0, step=0.5)
        
    with col2:
        pe, torque, crit = simulate_rapa_nui_road(s_mass, radius, tilt)
        st.metric("Swaying Pendulum Potential Energy", f"{pe/1e3:.2f} kJ")
        st.metric("Concave Track Restoring Torquing Matrix", f"{torque/1e3:.2f} kN·m")
        st.metric("Critical System Tipping Threshold Limit", f"{crit:.1f} Degrees")
        if tilt < crit:
            st.success(f"Stability Audit: SAFE. Statue remains balanced inside track (Threshold: {crit:.1f}°).")
        else:
            st.error(f"Stability Audit: CRITICAL TILT. Center of mass has breached footprint vectors.")

# Node 6: Puma Punku Acoustic Filter Array
elif node == "Puma Punku Acoustic Filter Array (Bolivia)":
    st.header("🧱 Puma Punku Andesite H-Block Interference Array")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Lithic Structural Variables")
        s_depth = st.slider("Interlocking Cavity Slot Depth (Meters)", 0.05, 0.50, 0.15, step=0.01)
        test_freq = st.slider("Target Tectonic Frequency to Audit (Hz)", 10, 500, 120, step=5)
        st.subheader("Richter Tectonic Force Actuator")
        eq_mag = st.slider("Earthquake Magnitude (Richter Scale)", 4.0, 9.5, 7.5, step=0.1)
        eq_dist = st.slider("Distance to Epicenter Fault Node (km)", 1.0, 50.0, 10.0, step=1.0)
        
    with col2:
        db_loss = simulate_puma_punku_h_block(seismic_amplitude=1.0, frequency_hz=test_freq, slot_depth_m=s_depth)
        pga, raw_stress = calculate_richter_pga_stress(eq_mag, eq_dist)
        
        dampening_factor = 10**(-db_loss / 20.0)
        mit_stress = raw_stress * dampening_factor
        safety = 25.0e6 / max(mit_stress, 1.0)
        
        st.metric("Acoustic Amplitude Attenuation", f"{db_loss:.2f} dB")
        st.metric("Peak Ground Acceleration Vector (PGA)", f"{pga:.3f} g")
        st.metric("Raw Unmitigated Tectonic Stress", f"{raw_stress / 1e3:.2f} kPa")
        st.metric("Mitigated Structural Outflow Stress", f"{mit_stress / 1e3:.2f} kPa")
        
        if safety > 1.0:
            st.success(f"System Integrity Matrix: SAFE. Structural Safety Factor: {safety:.2f}x.")
        else:
            st.error(f"System Critical Stress Warning: Yield risk. Safety Factor: {safety:.2f}x.")
        
        freq_x, atten_y = generate_puma_punku_curve(s_depth)
        fig, ax = plt.subplots(figsize=(6, 2.8))
        ax.plot(freq_x, atten_y, color='#9B59B6', linewidth=2.5)
        ax.axvline(x=test_freq, color='#E74C3C', linestyle='--')
        ax.set_title("Seismic Vibration Cancellation vs. Wave Frequency")
        ax.set_xlabel("Bedrock Seismic Frequency (Hz)")
        ax.set_ylabel("Dampening Effectiveness (Decibels Loss)")
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)
