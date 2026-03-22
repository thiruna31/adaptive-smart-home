"""
Adaptive Smart Environment Controller - Web Dashboard.

Run this file directly to start the app:
    python FuzzySmartHome/app.py
"""

import sys
import os

# --- AUTO-LAUNCHER ---
if __name__ == "__main__":
    if "streamlit" not in sys.modules:
        try:
            from streamlit.web import cli as stcli
        except ImportError:
            os.system("pip install streamlit")
            from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", __file__]
        sys.exit(stcli.main())

# --- APP LOGIC STARTS HERE ---
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Adjust path to find the engine
try:
    from fuzzy_logic_engine import FuzzyACEngine
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from fuzzy_logic_engine import FuzzyACEngine

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Adaptive Smart Home Controller",
    page_icon="🌡️",
    layout="wide"
)

# --- HEADER ---
st.title("🌡️ Adaptive Smart Home Controller")
st.markdown("""
**Research Objective:**  
To demonstrate an **Autonomous Energy Management System (AEMS)** that optimizes HVAC power consumption using **Mamdani Fuzzy Inference**. 

**Key Value Proposition:**
Unlike traditional "Threshold-based" thermostats (ON/OFF), this AI controller provides **smooth, continuous modulation** of cooling power based on multiple conflicting variables (Temp, Humidity, Occupancy). This results in:
1.  **Energy Efficiency**: Prevents short-cycling and over-cooling.
2.  **Thermal Comfort**: Adapts to "feels-like" temperature (heat index) rather than just dry bulb temperature.
3.  **Scalability**: Logic can be deployed on edge devices (Raspberry Pi/Microcontrollers).
""")
st.divider()

# --- SIDEBAR: SENSORS (INPUTS) ---
st.sidebar.header("1. Environmental Sensors")
st.sidebar.info("Simulate real-time sensor data feeds.")

temperature = st.sidebar.slider("Ambient Temperature (°C)", 10, 45, 25, help="Input from localized thermal sensors.")
humidity = st.sidebar.slider("Relative Humidity (%)", 0, 100, 50, help="Input from hygrometers. High humidity increases 'feels-like' temp.")
occupancy = st.sidebar.slider("Active Occupancy (People)", 0, 10, 2, help="Input from PIR/Infrared motion counters.")

# --- ENGINE COMPUTATION ---
result_power = 0.0
SIM_ERROR = None

try:
    engine = FuzzyACEngine()
    sim = engine.get_simulation()

    sim.input['temperature'] = temperature
    sim.input['humidity'] = humidity
    sim.input['occupancy'] = occupancy

    sim.compute()
    result_power = sim.output['ac_power']

except Exception as e:
    SIM_ERROR = str(e)
    # Default to 0 if error
    result_power = 0.0

# --- OUTPUTS (Main Area) ---
st.subheader("2. System Decisions (Inference Output)")

col1, col2, col3 = st.columns(3)

# Metric 1: AC Power
col1.metric("AC Compressor Load", f"{result_power:.1f}%", help="Frequency modulation (0-100%).")

# Metric 2: Status
status = "STANDBY"
if result_power > 85: 
    status = "⚠️ TURBO COOLING"
elif result_power > 60: 
    status = "⬆️ HIGH DEMAND"
elif result_power > 30: 
    status = "➡️ COMFORT MODE"
elif result_power > 5: 
    status = "⬇️ ECO SAVING"

col2.metric("Operational State", status)

# Metric 3: Watts (Estimated)
watts = (result_power / 100) * 3500  # Max 3500W
cost_est = (watts/1000) * 0.15 * 24 # $0.15/kWh for 24h
col3.metric("Est. Power Draw", f"{int(watts)} W", f"${cost_est:.2f}/day")

if SIM_ERROR:
    st.error(f"Inference Engine Failure: {SIM_ERROR}")

st.divider()

# --- VISUALIZATION ---
st.subheader("3. Explainable AI (XAI) Analysis")
st.write("Visualizing the **Aggregate Fuzzy Set**. The black line represents the **Centroid Defuzzification**, which converts the qualitative inference into a precise control signal.")

if st.checkbox("Show Logic Visualization", value=True):
    try:
        # Create figure for the AC Power output
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # We need to manually call .view(sim=sim)
        try:
           engine.ac_power.view(sim=sim)
            # Display in Streamlit
           st.pyplot(plt.gcf())
        except:
           pass # Sometimes skfuzzy throws warnings on non-interactive backends

        # Clear memory
        plt.clf() 
        plt.close(fig)
        
    except Exception as e:
        st.warning(f"Visualization not available: {e}")

# Footer
st.markdown("---")
st.caption("Adaptive Smart Environment Controller v2.0 | Accurate Mamdani Inference")
