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
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING & INTRO ---
st.title("❄️ Adaptive Energy Management System")
st.markdown("### `System Status: ONLINE` | `Mode: Autonomous`")

with st.expander("ℹ️  System Architecture & Research Abstract", expanded=False):
    st.markdown("""
    **Objective:** Optimize HVAC energy consumption while maintaining thermal comfort.
    
    **Methodology:** 
    This system utilizes a **Mamdani Fuzzy Inference System (FIS)**. Unlike binary (ON/OFF) controllers, it computes a continuous variable output (0-100%) based on linguistic rules.
    
    **Inference Process:**
    1.  **Fuzzification**: Converts crisp sensor inputs (e.g., 25°C) into fuzzy membership degrees (e.g., 0.8 'Warm').
    2.  **Rule Evaluation**: Applies logical rules (e.g., *IF Warm AND Humid THEN High Cooling*).
    3.  **Aggregation**: Combines the results of all active rules.
    4.  **Defuzzification**: Converts the aggregated fuzzy set into a single crisp output using the **Centroid Method**.
    """)

st.divider()

# --- SIDEBAR: SENSORS (INPUTS) ---
st.sidebar.header("🎛️ Sensor Inputs")
st.sidebar.markdown("Simulate environmental conditions.")

# Input Sliders
temp = st.sidebar.slider("🌡️ Temperature (°C)", 10.0, 45.0, 26.0, 0.5)
hum = st.sidebar.slider("💧 Humidity (%)", 0, 100, 60, 1)
occ = st.sidebar.slider("👥 Occupancy (People)", 0, 10, 2, 1)

st.sidebar.markdown("---")
st.sidebar.caption("Adaptive Controller v2.1")

# --- ENGINE COMPUTATION ---
try:
    # Initialize Engine (Cached in session state if needed, but fast enough to re-init)
    engine = FuzzyACEngine()
    
    # Compute Output
    power_output = engine.compute(temp, hum, occ)
    
    # Retrieve simulation state for visualization
    sim = engine.get_simulation()
    vars_ = engine.get_variables()

except Exception as e:
    st.error(f"Critical System Failure: {e}")
    st.stop()

# --- DASHBOARD ROW 1: METRICS ---
col1, col2, col3 = st.columns(3)

# 1. Power Output Metric
current_watts = (power_output / 100) * 3500  # Max 3500W system
with col1:
    st.metric(label="Compressor Load", value=f"{power_output:.1f}%")
    st.progress(int(power_output) / 100)

# 2. Operational State Metric
state_label = "IDLE"
state_emoji = "💤"

if power_output > 0:
    if power_output < 30:
        state_label = "ECO / LOW"
        state_emoji = "🍃"
    elif power_output < 70:
        state_label = "BALANCED"
        state_emoji = "⚖️"
    elif power_output < 90:
        state_label = "HIGH COOLING"
        state_emoji = "❄️"
    else:
        state_label = "MAX POWER"
        state_emoji = "🚀"

with col2:
    st.metric(label="Operational Mode", value=f"{state_label} {state_emoji}")
    st.caption(f"System logic has determined this is the optimal state.")

# 3. Cost Estimate Metric
kwh_cost = 0.15 # $0.15 per kWh
daily_cost = (current_watts / 1000) * 24 * kwh_cost
with col3:
    st.metric(label="Est. Power Draw", value=f"{int(current_watts)} W", delta=f"${daily_cost:.2f} / day")

st.divider()

# --- VISUALIZATION SECTION ---
st.subheader("📊 Real-time Logic Analysis")

st.markdown("Monitor the internal decision-making process.")

tab1, tab2 = st.tabs(["Decision Surface (Output)", "Sensor Activation (Inputs)"])

# Visualization Helper
def plot_fuzzy_var(variable, simulation, title):
    try:
        fig, ax = plt.subplots(figsize=(8, 3))
        variable.view(sim=simulation)
        plt.title(title)
        return fig
    except Exception as e:
        st.warning(f"Could not plot {title}: {e}")
        return None

with tab1:
    st.markdown("#### Aggregated Output & Defuzzification")
    st.caption("The black line represents the **Center of Gravity (Centroid)**, which is the final crisp output sent to the AC unit.")
    
    # Plotting Consequent
    try:
        # Create figure explicitly to avoid global state issues
        # engine.ac_power is the Consequent object
        # calling .view(sim=sim) populates the current figure
        fig, ax = plt.subplots(figsize=(10, 4))
        vars_['ac_power'].view(sim=sim)
        st.pyplot(fig)
        plt.close(fig) # Clean up
    except Exception as e:
        st.error(f"Visualization Error: {e}")

with tab2:
    st.markdown("#### Input Membership Activation")
    st.caption("See which linguistic terms (Cold, Warm, Hot, etc.) are triggered by current sensor values.")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("**Temperature**")
        fig = plot_fuzzy_var(vars_['temperature'], sim, "")
        if fig: st.pyplot(fig); plt.close(fig)

    with c2:
        st.markdown("**Humidity**")
        fig = plot_fuzzy_var(vars_['humidity'], sim, "")
        if fig: st.pyplot(fig); plt.close(fig)

    with c3:
        st.markdown("**Occupancy**")
        fig = plot_fuzzy_var(vars_['occupancy'], sim, "")
        if fig: st.pyplot(fig); plt.close(fig)

