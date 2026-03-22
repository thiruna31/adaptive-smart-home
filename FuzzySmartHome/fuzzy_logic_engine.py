import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Tuple, Dict, Any

class FuzzyACEngine:

    def __init__(self):
        self._init_variables()
        self._init_membership_functions()
        self._init_rules()
        self._build_control_system()

    def _init_variables(self):
        """Define the Antecedents and Consequent with their respective universes of discourse."""
        # 1. Inputs (Antecedents)
        # Temperature Range: 10°C to 45°C
        self.temperature = ctrl.Antecedent(np.arange(10, 46, 1), 'temperature')
        # Humidity Range: 0% to 100%
        self.humidity = ctrl.Antecedent(np.arange(0, 101, 1), 'humidity')
        # Occupancy Range: 0 to 10 people
        self.occupancy = ctrl.Antecedent(np.arange(0, 11, 1), 'occupancy')

        # 2. Output (Consequent)
        # AC Power Range: 0% to 100%
        self.ac_power = ctrl.Consequent(np.arange(0, 101, 1), 'ac_power')
        
        # Set Defuzzification Method: 'centroid' (Center of Gravity)
        # This provides a smooth, continuous control signal suitable for PID-like behavior.
        self.ac_power.defuzzify_method = 'centroid'

    def _init_membership_functions(self):
        """
        Define Membership Functions (MFs) for all fuzzy variables.
        Using Trapezoidal (trapmf) for boundaries and Triangular (trimf) for intermediates.
        """
        
        # --- Temperature MFs ---
        self.temperature['cold'] = fuzz.trapmf(self.temperature.universe, [10, 10, 16, 20])
        self.temperature['comfortable'] = fuzz.trimf(self.temperature.universe, [18, 22, 26])
        self.temperature['warm'] = fuzz.trimf(self.temperature.universe, [24, 28, 32])
        self.temperature['hot'] = fuzz.trapmf(self.temperature.universe, [30, 36, 45, 45])

        # --- Humidity MFs ---
        self.humidity['dry'] = fuzz.trimf(self.humidity.universe, [0, 0, 40])
        self.humidity['pleasant'] = fuzz.trimf(self.humidity.universe, [30, 50, 70])
        self.humidity['humid'] = fuzz.trimf(self.humidity.universe, [60, 100, 100])

        # --- Occupancy MFs ---
        self.occupancy['low'] = fuzz.trimf(self.occupancy.universe, [0, 0, 4])
        self.occupancy['moderate'] = fuzz.trimf(self.occupancy.universe, [3, 5, 7])
        self.occupancy['high'] = fuzz.trimf(self.occupancy.universe, [6, 10, 10])

        # --- AC Power MFs (Output) ---
        self.ac_power['off'] = fuzz.trimf(self.ac_power.universe, [0, 0, 20])
        self.ac_power['low'] = fuzz.trimf(self.ac_power.universe, [10, 30, 50])
        self.ac_power['medium'] = fuzz.trimf(self.ac_power.universe, [40, 60, 80])
        self.ac_power['high'] = fuzz.trimf(self.ac_power.universe, [70, 85, 95])
        self.ac_power['maximum'] = fuzz.trimf(self.ac_power.universe, [90, 100, 100])

    def _init_rules(self):
        """
        Define the Inference Rule Base.
        Strategy: Exhaustive coverage using boolean logic (AND/OR) to prevent undefined states.
        """
        
        # --- Cold Region ---
        # Rule 1: Safety/Economy - If it's cold, AC is strictly OFF.
        rule1 = ctrl.Rule(self.temperature['cold'], self.ac_power['off'])

        # --- Comfortable Region ---
        # Rule 2: Ideal conditions or dry/empty - Off to save energy.
        rule2 = ctrl.Rule(self.temperature['comfortable'] & (self.occupancy['low'] | self.humidity['dry']), self.ac_power['off'])
        
        # Rule 3: Moderate load - Low cooling needed.
        rule3 = ctrl.Rule(self.temperature['comfortable'] & self.occupancy['moderate'], self.ac_power['low'])

        # Rule 4: Latent heat load (Humidity) or High Occupancy - Increase to Medium.
        rule4 = ctrl.Rule(self.temperature['comfortable'] & (self.occupancy['high'] | self.humidity['humid']), self.ac_power['medium'])

        # --- Warm Region ---
        # Rule 5: Low load - Low cooling.
        rule5 = ctrl.Rule(self.temperature['warm'] & (self.occupancy['low'] | self.humidity['dry']), self.ac_power['low'])

        # Rule 6: Standard warm conditions - Medium cooling.
        rule6 = ctrl.Rule(self.temperature['warm'] & self.humidity['pleasant'], self.ac_power['medium'])

        # Rule 7: High load (People or Humidity) - High cooling.
        rule7 = ctrl.Rule(self.temperature['warm'] & (self.occupancy['high'] | self.humidity['humid']), self.ac_power['high'])

        # --- Hot Region ---
        # Rule 8: Low load - High cooling is still needed due to ambient temp.
        rule8 = ctrl.Rule(self.temperature['hot'] & (self.occupancy['low'] | self.humidity['dry']), self.ac_power['high'])

        # Rule 9: Critical load - Maximum cooling.
        rule9 = ctrl.Rule(self.temperature['hot'] & (self.occupancy['high'] | self.humidity['humid']), self.ac_power['maximum'])
        
        # Rule 10: Standard hot conditions - High cooling.
        rule10 = ctrl.Rule(self.temperature['hot'] & self.humidity['pleasant'], self.ac_power['high'])

        self.rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10]

    def _build_control_system(self):
        """Compile the rules into a ControlSystem and create the Simulation."""
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulation = ctrl.ControlSystemSimulation(self.control_system)

    def get_simulation(self) -> ctrl.ControlSystemSimulation:
        """Returns the active simulation object ready for computing."""
        return self.simulation

    def get_variables(self) -> Dict[str, Any]:
        """Returns a dictionary of the fuzzy variables for visualization purposes."""
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'occupancy': self.occupancy,
            'ac_power': self.ac_power
        }

def create_fuzzy_system() -> Tuple[ctrl.ControlSystemSimulation, Dict[str, Any]]:
    """
    Factory function for backward compatibility and easy initialization.
    
    Returns:
        simulation (ControlSystemSimulation): The ready-to-use fuzzy logic processor.
        variables (dict): The dictionary of Antecedents and Consequents.
    """
    engine = FuzzyACEngine()
    return engine.get_simulation(), engine.get_variables()

if __name__ == "__main__":
    # Self-test routine
    print("[INFO] Initializing Fuzzy Logic Engine...")
    sim, vars_ = create_fuzzy_system()
    print(f"[SUCCESS] Engine initialized with {len(vars_)} variables.")
    print("[INFO] Ready for simulation.")
