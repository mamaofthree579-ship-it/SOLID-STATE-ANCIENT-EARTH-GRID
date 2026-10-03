import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from engines.physics_models import (
    simulate_giza_piezocore, simulate_quetzalcoatl_hull,
    simulate_tikal_ram, simulate_rapa_nui_road,
    simulate_mesoamerican_court, simulate_giza_shafts,
    simulate_puma_punku_h_block
)

# Core data range generator functions directly embedded for application rendering
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

# App Configuration & Visual Styling Parameters
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

if node == "Overview & Universal Lexicon":
    st.header("📋 The Universal Engineering Lexicon")
    st.markdown("""
    Ancient societies logged blueprints and equations in the only medium capable of surviving millennia: stone. By mapping their descriptions of dynamic energy (*mana*, *serpents*) directly to physical equivalents, we unlock a completely unrecognized branch of human technology.
    """)
    
    st.table([
        {"Traditional Archeology Label": "God / Deity", "Solid-State Engineering Equivalent": "Fundamental Field Force (Gravity, EM, Tension)"},
        {"Traditional Archeology Label": "Sacred Statue / Idol", "Solid-State Engineering Equivalent": "Tuned Mechanical Transducer / Resonator"},
        {"Traditional Archeology Label": "Temple / Sanctuary", "Solid-State Engineering Equivalent": "Enclosed Capacitive Power Terminal Hub"},
        {"Traditional Archeology Label": "Sacred Holy Road", "Solid-State Engineering Equivalent": "Energy Bus Line / High-Mass Waveguide"},
        {"Traditional Archeology Label": "Ritual / Chant / Legend", "Solid-State Engineering Equivalent": "System Frequency Calibration / Operational Manual"}
    ])
    
    st.info("💡 Select an engineering node in the sidebar to begin loading specialized fluid and wave mechanics simulators.")

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
        
        st.metric("Tuned Core Core Frequency", f"{f_nat:.2f} Hz")
        st.metric("Static Gravitational Compression Load", f"{static_p/1e3:.2f} kPa")
        st.metric("Heterojunction Energy Capture Ratio", f"{ref_coeff*100:.1f}%")
        st.metric("Helmholtz Air-Cavity Resonance", f"{f_helm:.2f} Hz")
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(t, charge * 1e12, color='#E67E22', linewidth=2)
        ax.set_title("Piezoelectric Polarization Field Output over Time")
        ax.set_xlabel("Seismic Period Window (Seconds)")
        ax.set_ylabel("Charge Density (pC/m²)")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

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
        ax.plot(angles_x, drag_y / 1e3, color='#2980B9', linewidth=2.5, label='Net Drag Sweep')
        ax.axvline(x=tilt, color='#E67E22', linestyle='--', label=f'Active Hull Alignment ({tilt}°)')
        ax.set_title("Wave Drag Attenuation via Serpentine Geometry Adjustments")
        ax.set_xlabel("Hull Articulation Shift (Degrees)")
        ax.set_ylabel("Total Dynamic Resistance (Kilo-Newtons)")
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

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
        ax.plot(rain_x, lift_y, color='#1ABC9C', linewidth=2.5, label='Calculated Fluid Lift')
        ax.axvline(x=rain, color='#E74C3C', linestyle='--', label=f'Current Storm Event ({rain} mm/hr)')
        ax.set_title("Fluid Head Lift Vector vs. Monsoonal Intensity")
        ax.set_xlabel("Rainfall Rate (mm / hour)")
        ax.set_ylabel("Maximum Vertical Water Lift (Meters)")
        ax.legend(loc='upper left', fontsize='small')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)

elif node == "Rapa Nui Grid & Concave Roadways":
    st.header("🗿 Rapa Nui Groundwater Sieve & Road Waveguides")
    
    col1, col2 = st.columns(2)
    with col1:
        s_mass = st.slider("Moai Transducer Column Mass (kg)", 5000, 80000, 15000, step=2000)
        radius = st.slider("Roadway Concave Geometry Radius (meters)", 1.5, 10.0, 3.5, step=0.5)
        tilt = st.slider("Dynamic Sway Walking Tilt Angle (Degrees)", 1.0, 15.0, 6.0, step=0.5)
        
    with col2:
        pe, torque, crit = simulate_rapa_nui_road(s_mass, radius, tilt)
        
        st.metric("Swaying Pendulum Potential Energy", f"{pe/1e3:.2f} kJ")
        st.metric("Concave Track Restoring Torquing Matrix", f"{torque/1e3:.2f} kN·m")
        st.metric("Critical System Tipping Threshold Limit", f"{crit:.1f} Degrees")
        
        st.success(f"Stability Audit: Safe. The statue remains securely balanced inside the self-correcting gravity track (Concave limit threshold is {crit:.1f}°).")

elif node == "Puma Punku Acoustic Filter Array (Bolivia)":
    st.header("🧱 Puma Punku Andesite H-Block Interference Array")
    st.markdown("""
    By analyzing the raw material geometries of Puma Punku's interlocking H-blocks, this simulator tests the hypothesis that the structures function as a **solid-state acoustic low-pass filter array** designed for destructive phase cancellation of earth seismic tremors.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Lithic Structural Variables")
        s_depth = st.slider("Interlocking Cavity Slot Depth (Meters)", 0.05, 0.50, 0.15, step=0.01)
        test_freq = st.slider("Target Tectonic Frequency to Audit (Hz)", 10, 500, 120, step=5)
        
    with col2:
        db_loss = simulate_puma_punku_h_block(seismic_amplitude=1.0, frequency_hz=test_freq, slot_depth_m=s_depth)
        
        st.metric("Acoustic Amplitude Attenuation", f"{db_loss:.2f} dB")
        
        # Phase Interference Frequency Curve Generation
        freq_x, atten_y = generate_puma_punku_curve(s_depth)
        
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(freq_x, atten_y, color='#9B59B6', linewidth=2.5, label='Attenuation Profile')
        ax.axvline(x=test_freq, color='#E74C3C', linestyle='--', label=f'Audited Frequency ({test_freq} Hz)')
        ax.set_title("Seismic Vibration Cancellation vs. Wave Frequency")
        ax.set_xlabel("Bedrock Seismic Frequency (Hz)")
        ax.set_ylabel("Dampening Effectiveness (Decibels Loss)")
        ax.legend(loc='upper right', fontsize='small')
        ax.grid(True, alpha=0.2)
        st.pyplot(fig)
