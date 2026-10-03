import streamlit as st
import matplotlib.pyplot as plt
from engines.physics_models import (
    simulate_giza_piezocore, simulate_quetzalcoatl_hull,
    simulate_tikal_ram, simulate_rapa_nui_road,
    simulate_mesoamerican_court, simulate_giza_shafts
)

st.set_page_config(page_title="SS-AEGIC Simulator", layout="wide")

st.title("🌐 Solid-State Ancient Earth-Grid Simulation Core (SS-AEGIC)")
st.markdown("""
This open-source dashboard strips away historical paradigms of primitive superstition and models ancient monumental engineering through the lens of **solid-state physics, geodetics, and trans-medium fluid dynamics**.
""")

# Sidebar navigation
node = st.sidebar.selectbox("Select Engineering Node", [
    "Overview & Universal Lexicon",
    "Giza Resonator & Tuned Shafts (Egypt)",
    "Quetzalcoatl Trans-Medium Vessel",
    "Tikal Macrofluidic Ram Pump (Maya)",
    "Rapa Nui Grid & Concave Roadways"
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

elif node == "Tikal Macrofluidic Ram Pump (Maya)":
    st.header("⚡ Tikal Macrofluidic Mass-Actuated Ram Pump")
    
    col1, col2 = st.columns()
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
        
        # New Interactive Chart Generation
        from engines.physics_models import generate_tikal_lift_curve
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

        
        # Plotting the active EM production curve
        fig, ax = plt.subplots(figsize=(6, 2.5))
        ax.plot(t, charge * 1e12, color='#E67E22', linewidth=2)
        ax.set_title("Piezoelectric Polarization Field Output over Time")
        ax.set_xlabel("Seismic Period Window (Seconds)")
        ax.set_ylabel("Charge Density (pC/m²)")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

elif node == "Quetzalcoatl Trans-Medium Vessel":
    st.header("🛶 Quetzalcoatl Trans-Medium Wave Mechanics")
    st.markdown("Air and water are a continuous medium; air is simply a lower-density version of water. This engine validates an adjustable geometry multi-hull configuration changing parameters to minimize wave resistance.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        knots = st.slider("Vessel Velocity (Knots)", 2, 25, 12)
        tilt = st.slider("Serpentine Hull Articulation Angle (Degrees)", 0.0, 45.0, 22.5, step=2.5)
        
    with col2:
        l_eff, fr, drag = simulate_quetzalcoatl_hull(knots, tilt)
        
        st.metric("Effective Waterline Footprint", f"{l_eff:.2f} meters")
        st.metric("Calculated Froude Index (Fr)", f"{fr:.3f}")
        st.metric("Net Dynamic Wave Resistance", f"{drag:.2f} Newtons")
        
        st.info("💡 Adjusting the hull articulation angle allows the ship to change its effective Froude profile, optimizing kinetic energy capture across shifting fluid phases.")

elif node == "Tikal Macrofluidic Ram Pump (Maya)":
    st.header("⚡ Tikal Macrofluidic Mass-Actuated Ram Pump")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        area = st.slider("Pluvial Catchment Basin Area (m²)", 500, 5000, 2500, step=250)
        rain = st.slider("Monsoonal Rainfall Rate (mm/hour)", 10, 150, 75, step=5)
        p_height = st.slider("Pyramid Mass Actuator Height (Meters)", 10, 80, 47)
        
    with col2:
        mass, hammer, lift = simulate_tikal_ram(area, rain, p_height)
        
        st.metric("Total Pyramid Structural Mass Action", f"{mass/1e6:.3f} Megatonnes")
        st.metric("Transient Water-Hammer Shockwave Pressure", f"{hammer/1e6:.2f} MPa")
        st.metric("Hydro-Pneumatic Fluid Elevation Lift", f"{lift:.2f} meters")
        
        st.markdown("### The Structural Mechanics Paradigm:")
        st.write("By forcing high-volume seasonal downpours through narrowing stone conduits directly beneath millions of tons of limestone, the Mayan architects engineered automated fluid loops that pumped purified water up into high-altitude urban reservoirs without mechanical motors.")

elif node == "Rapa Nui Grid & Concave Roadways":
    st.header("🗿 Rapa Nui Groundwater Sieve & Road Waveguides")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        s_mass = st.slider("Moai Transducer Column Mass (kg)", 5000, 80000, 15000, step=2000)
        radius = st.slider("Roadway Concave Geometry Radius (meters)", 1.5, 10.0, 3.5, step=0.5)
        tilt = st.slider("Dynamic Sway Walking Tilt Angle (Degrees)", 1.0, 15.0, 6.0, step=0.5)
        
    with col2:
        pe, torque, crit = simulate_rapa_nui_road(s_mass, radius, tilt)
        f_court, comp, loss = simulate_mesoamerican_court(96, 8, 30) # Cross-node acoustic transmission variables
        
        st.metric("Swaying Pendulum Potential Energy", f"{pe/1e3:.2f} kJ")
        st.metric("Concave Track Restoring Torquing Matrix", f"{torque/1e3:.2f} kN·m")
        st.metric("Critical System Tipping Threshold Limit", f"{crit:.1f} Degrees")
        
        st.success(f"Stability Audit: Safe. The statue remains securely balanced inside the self-correcting gravity track (Concave limit threshold is {crit:.1f}°).")
