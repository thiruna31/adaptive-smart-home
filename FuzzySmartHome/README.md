# Adaptive Smart Environment Controller (AEMS)

## 📌 Research Abstract

This project implements an **Autonomous Energy Management System (AEMS)** designed to optimize HVAC power consumption using **Mamdani Fuzzy Inference Systems (FIS)**. Traditional threshold-based thermostats operate on a binary ON/OFF logic, leading to energy inefficiency (short-cycling) and thermal discomfort (hysteresis). 

This solution introduces a continuous control loop that modulates AC compressor power (0-100%) based on a multi-variable analysis of:
1.  **Ambient Temperature** (°C)
2.  **Relative Humidity** (%)
3.  **Active Occupancy** (Person count)

By fuzzifying these crisp inputs into linguistic variables (e.g., *Comfortable*, *Humid*, *High Load*), the system imitates human reasoning to deliver precise, energy-efficient cooling.

---

## 🚀 Key Features (v2.1)

*   **Logic Engine**: A robust `FuzzyACEngine` class utilizing **Centroid Defuzzification** for smooth output control.
*   **Explainable AI (XAI)**:
    *   **Decision Surface Visualization**: Real-time plotting of the aggregated fuzzy set to explain *why* a specific power level was chosen.
    *   **Sensor Activation**: Visual feedback on which linguistic terms are currently active.
*   **Web Dashboard**: A professional `Streamlit` interface for real-time scenario simulation and parameter tuning.
*   **Modular Architecture**: Separation of concern between the Inference Engine (`fuzzy_logic_engine.py`) and the Interface (`app.py`).

---

## 🛠️ Installation

Prerequisites: Python 3.9+

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Vimeth22/adaptive-smart-home.git
    cd adaptive-smart-home
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Usage

### 1. Web Dashboard (Interactive Demo)
Launch the professional dashboard to interact with the logic engine in real-time.

```bash
streamlit run FuzzySmartHome/app.py
```
*Access the dashboard at `http://localhost:8501`*

### 2. CLI Benchmark Simulator
Run a predefined set of edge-case scenarios to validate system stability.

```bash
python FuzzySmartHome/simulator.py
```

---

## 📂 Project Structure

```
adaptive-smart-home/
├── FuzzySmartHome/
│   ├── app.py                  # Streamlit Web Dashboard (v2.1)
│   ├── fuzzy_logic_engine.py   # Core Mamdani Inference Logic
│   ├── simulator.py            # CLI Benchmarking Tool
│   └── requirements.txt        # Python Dependencies
├── .gitignore
└── README.md
```

---

## 🔬 Methodology

The system operates on a **Mamdani Inference** pipeline:

1.  **Fuzzification**: 
    - Inputs are mapped to fuzzy sets using Trapezoidal and Triangular membership functions.
2.  **Rule Evaluation**: 
    - 10 conditional rules (Knowledge Base) cover all operational states properly.
    - Example: *IF Temperature is Warm AND Humidity is High THEN AC Power is High.*
3.  **Aggregation**: 
    - The consequences of all active rules are combined into a single fuzzy set.
4.  **Defuzzification**: 
    - The **Center of Gravity (Centroid)** method allows for a precise "Crisp" output value (0-100%) to be sent to the AC inverter.

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).

