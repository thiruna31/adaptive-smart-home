# FuzzySmartHome - Adaptive Smart Environment Controller (Professional Edition)

This repository contains a Python-based Fuzzy Inference System (FIS) designed to optimize Air Conditioning (AC) power consumption. It leverages Mamdani fuzzy logic to handle non-linear relationships between temperature, humidity, and occupancy.

## Features (v2.0)

*   **Modular Architecture**: Encapsulated `FuzzyACEngine` class for robustness and reusability.
*   **Comprehensive Rule Base**: 10 logical rules covering all edge cases (Cold/Hot/Humid/Occupied) ensuring zero undefined states.
*   **Professional Simulation**: Benchmarking with detailed logging and error handling.
*   **Advanced Visualization**: Generates clear, annotated Matplotlib charts for membership functions and defuzzification (centroid).
*   **Type Safety**: Fully type-hinted codebase for better tooling support.

## Project Structure

*   `fuzzy_logic_engine.py`: The core inference engine (Antecedents, Consequents, Rules).
*   `simulator.py`: Test harness for running benchmarks and visualizations.
*   `requirements.txt`: Dependency manifest.

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the simulator to benchmark scenarios and view visualizations:

```bash
python simulator.py
```

## Benchmark Scenarios

The simulator executes the following predefined test cases:

1.  **Cold Empty Room** (12°C, 20%, 0 occ) -> Safety Off.
2.  **Hot Crowded Party** (35°C, 85%, 9 occ) -> Maximum Cooling.
3.  **Pleasant Study Session** (22°C, 45%, 2 occ) -> Eco/Low.
4.  **Warm Humid Day** (28°C, 75%, 4 occ) -> Medium/High Load handling.
5.  **Extreme Heat** (42°C, 30%, 1 occ) -> High Load handling (Ambient driven).

## License

Academic Use Only.

