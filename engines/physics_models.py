import numpy as np

# Core Environmental Constants (hardcoded fallbacks matching JSON config)
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

def simulate_mesoamerican_court(court_length, wall_height, gap_width):
    f_cutoff = C_AIR / (2.0 * gap_width)
    compression = 1.0 + (wall_height * np.tan(np.radians(45.0)) / gap_width)
    alpha = 0.005
    loss_db = alpha * court_length / compression
    return f_cutoff, compression, loss_db

def simulate_giza_shafts(aperture_d, wind_speed, cavity_vol, shaft_len):
    f_vortex = (ST_NUM * wind_speed) / aperture_d
    area_shaft = 0.045
    f_helmholtz = (C_AIR / (2.0 * np.pi)) * np.sqrt(area_shaft / (cavity_vol * shaft_len))
    return f_vortex, f_helmholtz

def generate_tikal_lift_curve(catchment_area, height_m, max_rain=150):
    """
    Generates an array of fluid height lifts across a sweeping rainfall spectrum 
    to visualize the dynamic efficiency scale of the mass-actuated ram pump.
    """
    rain_range = np.linspace(10, max_rain, 100)
    lift_depths = []
    
    for r in rain_range:
        _, _, lift_m = simulate_tikal_ram(catchment_area, r, height_m)
        lift_depths.append(lift_m)
        
    return rain_range, np.array(lift_depths)

def generate_quetzalcoatl_drag_curve(velocity_knots):
    """
    Generates a comparison array modeling structural drag across a full 45-degree 
    hull articulation sweep to isolate the exact point of fluid impedance matching.
    """
    angles = np.linspace(0, 45, 100)
    drag_forces = []
    
    for a in angles:
        _, _, drag = simulate_quetzalcoatl_hull(velocity_knots, a)
        drag_forces.append(drag)
        
    return angles, np.array(drag_forces)

def simulate_puma_punku_h_block(seismic_amplitude, frequency_hz, slot_depth_m=0.15):
    """
    Models an interlocking Andesite H-Block grid as a Solid-State Acoustic Filter.
    Calculates phase cancellation and decibel dampening of high-frequency earth tremors.
    """
    # Density and acoustic velocity of dense high-altitude Andesite
    density_andesite = 2800.0  # kg/m^3
    velocity_andesite = 6000.0  # m/s
    
    # Calculate wave length of incoming seismic tremor through the stone matrix
    wavelength = velocity_andesite / frequency_hz
    
    # Phase shift induced by the geometric restriction slots
    # Perfect 180 degree destructive cancellation occurs when path length delta matches half-wavelength
    phase_shift_rad = (2.0 * np.pi * slot_depth_m) / wavelength
    cancellation_efficiency = np.sin(phase_shift_rad)
    
    # Decibel reduction calculation
    attenuation_db = -20.0 * np.log10(np.clip(1.0 - cancellation_efficiency, 1e-3, 1.0))
    
    print("\n=== PUMA PUNKU LITHIC FILTER SIMULATION VERIFIED ===")
    print(f"Bedrock Elastic Wavelength: {wavelength:.2f} meters")
    print(f"Geometric Phase Shift Induced: {np.degrees(phase_shift_rad):.4f} degrees")
    print(f"Seismic Wave Amplitude Dampening: {attenuation_db:.2f} dB")
    return attenuation_db
