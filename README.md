

# Adaptive Smart Environment Controller

### Mamdani Fuzzy Logic Approach for Intelligent HVAC Energy Management

## Overview

This project presents an **Adaptive Smart Environment Controller** that replaces traditional binary (ON/OFF) thermostat systems with an intelligent **Mamdani Fuzzy Inference System (FIS)**. The controller dynamically adjusts air-conditioning compressor power between **0% and 100%** based on environmental conditions.

Unlike conventional controllers that cause temperature fluctuations and energy waste, this system provides smooth, proportional responses using fuzzy logic reasoning derived from human decision-making patterns.

The controller evaluates three environmental parameters:

* Temperature
* Humidity
* Occupancy

to generate optimal cooling power for improved comfort and reduced energy consumption.

---

## Objectives

The primary objectives of this project are:

* Reduce HVAC energy consumption
* Improve indoor thermal comfort
* Eliminate compressor short cycling
* Provide explainable AI-based decision transparency
* Implement a multi-input fuzzy logic control system
* Demonstrate practical computational intelligence application in smart homes

---

## System Inputs

The fuzzy controller processes three input variables representing indoor environmental conditions.

### Temperature (°C)

Linguistic categories:

* Cold
* Comfortable
* Warm
* Hot

Operating range:

10°C – 45°C

---

### Humidity (%)

Linguistic categories:

* Dry
* Pleasant
* Humid

Operating range:

0% – 100%

---

### Occupancy Level

Linguistic categories:

* Low
* Moderate
* High

Operating range:

0 – 10 persons

---

## System Output

The output variable represents compressor power level.

### AC Power (%)

Linguistic categories:

* Off
* Low
* Medium
* High
* Maximum

Operating range:

0% – 100%

This enables gradual cooling adjustments instead of abrupt ON/OFF switching.

---

## Mamdani Fuzzy Inference Process

The controller follows four inference stages:

1. Fuzzification
2. Rule Evaluation
3. Aggregation
4. Centroid Defuzzification

Centroid defuzzification ensures smooth transitions in compressor power output and minimizes mechanical wear.

---

## Fuzzy Rule Base

The system uses a knowledge base of expert-defined fuzzy rules to determine cooling response.

Example rules include:

* IF Temperature is Cold → Power OFF
* IF Comfortable AND Moderate Occupancy → Power LOW
* IF Warm AND Humid → Power HIGH
* IF Hot AND High Occupancy → Power MAXIMUM

These rules enable intelligent adaptation across multiple environmental conditions.

---

## Energy Efficiency Benefits

Compared with conventional thermostats, the fuzzy controller:

* Reduces unnecessary compressor activation
* Eliminates temperature oscillations
* Prevents short cycling
* Improves thermal stability
* Reduces energy usage during moderate load conditions

Experimental evaluation demonstrates measurable energy savings during warm and humid scenarios.

---

## Software Architecture

The system consists of two major components.

### Fuzzy Inference Engine

Implements:

* membership functions
* rule evaluation logic
* aggregation
* centroid defuzzification

Built using scientific Python libraries for numerical efficiency and accuracy.

---

### Interactive Visualization Dashboard

A web-based interface enables:

* real-time sensor simulation
* dynamic fuzzy membership visualization
* power output monitoring
* explainable decision transparency

This supports interpretability of controller behavior.

---

## Benchmark Scenario Results

Representative simulation outputs demonstrate controller behavior:

| Scenario               | Temperature | Humidity | Occupancy | Power Output |
| ---------------------- | ----------- | -------- | --------- | ------------ |
| Cold Empty Room        | 12°C        | 20%      | 0         | 0%           |
| Pleasant Study Session | 22°C        | 45%      | 2         | 7.78%        |
| Warm Humid Day         | 28°C        | 75%      | 4         | 82.93%       |
| Hot Crowded Room       | 35°C        | 85%      | 9         | 96.50%       |
| Extreme Heat Condition | 42°C        | 30%      | 1         | 83.25%       |

These results confirm adaptive power scaling across diverse environmental conditions.

---

## Technologies Used

The implementation combines computational intelligence techniques with modern Python tools:

* Python
* Fuzzy Logic Control Systems
* NumPy
* scikit-fuzzy
* Matplotlib
* Streamlit

---

## Applications

This system can be applied in:

* Smart homes 🏠
* Intelligent HVAC systems 🌡️
* Energy-efficient buildings ⚡
* IoT automation platforms 📡
* Adaptive climate control environments 🌍

---

## Key Contributions

This project demonstrates:

* Multi-input Mamdani fuzzy controller design
* Continuous compressor modulation strategy
* Ten-rule expert knowledge base implementation
* Explainable AI visualization framework
* Energy-efficient HVAC automation model

---

## Future Enhancements

Possible improvements include:

* adaptive membership tuning using machine learning
* multi-zone climate control integration
* IoT sensor connectivity
* reinforcement learning optimization
* embedded controller deployment for real-time environments

---

## Authors

**Vimeth Jayawardana**
Department of Computer Science
Georgia State University

**Thirunavukkarasu Palaniappa**
Department of Computer Science
Georgia State University


