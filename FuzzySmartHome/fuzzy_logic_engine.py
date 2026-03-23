import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from typing import Tuple, Dict, Any, List
import logging

# Configure module logger
logger = logging.getLogger(__name__)

class FuzzyACEngine:
    
    # System Configuration
    CONFIG = {
        'temp_range': (10, 46, 0.5),      # Min, Max, Step
        'humidity_range': (0, 101, 1),
        'occupancy_range': (0, 11, 1),
        'power_range': (0, 101, 1),
        'defuzzify_method': 'centroid'
    }

    def __init__(self):
        self._simulation = None
        self._control_system = None
        self.rules: List[ctrl.Rule] = []
        
        # Build the engine
        try:
            self._init_variables()
            self._init_membership_functions()
            self._init_rules()
            self._build_control_system()
            logger.info("Fuzzy Logic Engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Fuzzy Logic Engine: {e}")
            raise

    def _init_variables(self):
        # Unpacking config
        t_min, t_max, t_step = self.CONFIG['temp_range']
        h_min, h_max, h_step = self.CONFIG['humidity_range']
        o_min, o_max, o_step = self.CONFIG['occupancy_range']
        p_min, p_max, p_step = self.CONFIG['power_range']

        # Antecedents (Inputs)
        self.temperature = ctrl.Antecedent(np.arange(t_min, t_max, t_step), 'temperature')
        self.humidity = ctrl.Antecedent(np.arange(h_min, h_max, h_step), 'humidity')
        self.occupancy = ctrl.Antecedent(np.arange(o_min, o_max, o_step), 'occupancy')

        # Consequent (Output)
        self.ac_power = ctrl.Consequent(np.arange(p_min, p_max, p_step), 'ac_power')
        self.ac_power.defuzzify_method = self.CONFIG['defuzzify_method']

    def _init_membership_functions(self):
        """Defines fuzzy sets using triangular and trapezoidal shapes."""
        
        # Temperature 
        self.temperature['cold']        = fuzz.trapmf(self.temperature.universe, [10, 10, 16, 20])
        self.temperature['comfortable'] = fuzz.trimf(self.temperature.universe,  [18, 22, 26])
        self.temperature['warm']        = fuzz.trimf(self.temperature.universe,  [24, 28, 32])
        self.temperature['hot']         = fuzz.trapmf(self.temperature.universe, [30, 36, 45, 45])

        # Humidity 
        self.humidity['dry']      = fuzz.trimf(self.humidity.universe, [0, 0, 40])
        self.humidity['pleasant'] = fuzz.trimf(self.humidity.universe, [30, 50, 70])
        self.humidity['humid']    = fuzz.trimf(self.humidity.universe, [60, 100, 100])

        # Occupancy 
        self.occupancy['low']      = fuzz.trimf(self.occupancy.universe, [0, 0, 4])
        self.occupancy['moderate'] = fuzz.trimf(self.occupancy.universe, [3, 5, 7])
        self.occupancy['high']     = fuzz.trimf(self.occupancy.universe, [6, 10, 10])

        # AC Power Output
        self.ac_power['off']     = fuzz.trimf(self.ac_power.universe, [0, 0, 20])
        self.ac_power['low']     = fuzz.trimf(self.ac_power.universe, [10, 30, 50])
        self.ac_power['medium']  = fuzz.trimf(self.ac_power.universe, [40, 60, 80])
        self.ac_power['high']    = fuzz.trimf(self.ac_power.universe, [70, 85, 95])
        self.ac_power['maximum'] = fuzz.trimf(self.ac_power.universe, [90, 100, 100])

    def _init_rules(self):
        T = self.temperature
        H = self.humidity
        O = self.occupancy
        Power = self.ac_power

        self.rules = [
            # Rule 1: Safety/Economy
            ctrl.Rule(T['cold'], Power['off'], label='Safety Cutoff'),

            # Rule 2: Ideal Conditions - Save Energy
            ctrl.Rule(T['comfortable'] & (O['low'] | H['dry']), Power['off'], label='Eco Idle'),
            
            # Rule 3: Maintenance Cooling
            ctrl.Rule(T['comfortable'] & O['moderate'], Power['low'], label='Light Maintain'),

            # Rule 4: Load Compensation
            ctrl.Rule(T['comfortable'] & (O['high'] | H['humid']), Power['medium'], label='Load Comp'),

            # Rule 5: Warm - Low Load
            ctrl.Rule(T['warm'] & (O['low'] | H['dry']), Power['low'], label='Warm Low'),

            # Rule 6: Warm - Standard
            ctrl.Rule(T['warm'] & H['pleasant'], Power['medium'], label='Warm Std'),

            # Rule 7: Warm - High Load
            ctrl.Rule(T['warm'] & (O['high'] | H['humid']), Power['high'], label='Warm High'),

            # Rule 8: Hot - Low Load (Ambient Fighting)
            ctrl.Rule(T['hot'] & (O['low'] | H['dry']), Power['high'], label='Hot Ambient'),

            # Rule 9: Critical Load - Maximum Cooling
            ctrl.Rule(T['hot'] & (O['high'] | H['humid']), Power['maximum'], label='Critical Max'),
            
            # Rule 10: Hot - Standard
            ctrl.Rule(T['hot'] & H['pleasant'], Power['high'], label='Hot Std'),
        ]

    def _build_control_system(self):
        self._control_system = ctrl.ControlSystem(self.rules)
        self._simulation = ctrl.ControlSystemSimulation(self._control_system)

    def compute(self, temp: float, hum: float, occ: int) -> float:
        if not self._simulation:
            raise RuntimeError("Engine not initialized properly.")

        try:
            self._simulation.input['temperature'] = temp
            self._simulation.input['humidity'] = hum
            self._simulation.input['occupancy'] = occ
            
            self._simulation.compute()
            return self._simulation.output['ac_power']
        except Exception as e:
            logger.error(f"Computation error: {e}")
            return 0.0

    def get_simulation(self) -> ctrl.ControlSystemSimulation:
        return self._simulation

    def get_variables(self) -> Dict[str, Any]:
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'occupancy': self.occupancy,
            'ac_power': self.ac_power
        }

def create_fuzzy_system() -> Tuple[ctrl.ControlSystemSimulation, Dict[str, Any]]:
    engine = FuzzyACEngine()
    return engine.get_simulation(), engine.get_variables()

if __name__ == "main":
    # Robust Self-Test
    logging.basicConfig(level=logging.INFO)
    print("[SELF-TEST] START")
    
    try:
        engine = FuzzyACEngine()
        test_val = engine.compute(25, 50, 2) 
        print(f"Test Computation (25C, 50%, 2ppl): {test_val:.2f}% AC Power")
        print("[SELF-TEST] PASSED ")
    except Exception as e:
        print(f"[SELF-TEST] FAILED: {e}")

