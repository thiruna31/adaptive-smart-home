import matplotlib.pyplot as plt
import numpy as np
import logging
import time
from fuzzy_logic_engine import create_fuzzy_system
from typing import Dict, Any

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("SmartHomeSimulator")

class SmartHomeSimulator:
    """
    Handles the execution of test scenarios and visualization of results
    for the Fuzzy AC Control System.
    """

    def __init__(self):
        """Initialize the simulator and load the fuzzy engine."""
        logger.info("Initializing Smart Home Simulator...")
        try:
            self.simulation, self.variables = create_fuzzy_system()
            logger.info("Fuzzy Logic Engine loaded successfully.")
        except Exception as e:
            logger.critical(f"Failed to load Fuzzy Logic Engine: {e}")
            raise

    def simulate_scenario(self, temp: float, humidity: float, occupancy: int) -> float:
        """
        Computes the Defuzzified AC Power percentage for a single input vector.

        Args:
            temp (float): Temperature in Celsius.
            humidity (float): Relative Humidity (0-100%).
            occupancy (int): Number of people.

        Returns:
            float: Defuzzified AC Power Output (0-100%).
        """
        try:
            # Set inputs
            self.simulation.input['temperature'] = temp
            self.simulation.input['humidity'] = humidity
            self.simulation.input['occupancy'] = occupancy

            # Compute fuzzy inference
            self.simulation.compute()

            result = self.simulation.output['ac_power']
            if np.isnan(result):
                logger.warning(f"Result is NaN for inputs: T={temp}, H={humidity}, O={occupancy}")
                return 0.0
            return result
        except Exception as e:
            logger.error(f"Error during simulation (T={temp}, H={humidity}, O={occupancy}): {e}")
            return 0.0

    def run_benchmark(self):
        """
        Runs a suite of standard test scenarios to validate system behavior.
        """
        scenarios = [
            ("Cold Empty Room", 12, 20, 0),
            ("Hot Crowded Party", 35, 85, 9),
            ("Pleasant Study Session", 22, 45, 2),
            ("Warm Humid Day", 28, 75, 4),  # Additional test case
            ("Extreme Heat", 42, 30, 1)     # Additional test case
        ]

        logger.info("Starting Benchmark Simulation...")
        print("\n" + "="*80)
        print(f"{'SCENARIO NAME':<25} | {'TEMP (°C)':<10} | {'HUM (%)':<8} | {'OCC (p)':<8} | {'AC POWER (%)':<15}")
        print("-" * 80)

        results = []
        for name, t, h, o in scenarios:
            power = self.simulate_scenario(t, h, o)
            results.append((name, power))
            print(f"{name:<25} | {t:<10} | {h:<8} | {o:<8} | {power:.2f}%")
        
        print("="*80 + "\n")
        logger.info("Benchmark complete.")
        return results

    def visualize_system(self):
        logger.info("Generating System Visualizations...")

        # Plot 1: Temperature MFs
        try:
            self.variables['temperature'].view()
            plt.title("Antecedent: Temperature Membership Functions")
            plt.ylabel("Membership Degree (u)")
            plt.xlabel("Temperature (°C)")
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Plot 2: AC Power MFs (Consequent)
            self.variables['ac_power'].view()
            plt.title("Consequent: AC Power Membership Functions")
            plt.ylabel("Membership Degree (u)")
            plt.xlabel("Power Output (%)")
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Plot 3: Defuzzification Example (Hot Crowded Party)
            # We re-run the compute to ensure the state is correct for the .view(sim=simulation) call
            test_case = {'temperature': 35, 'humidity': 85, 'occupancy': 9}
            logger.info(f"Visualizing Defuzzification for inputs: {test_case}")
            
            self.simulation.input['temperature'] = test_case['temperature']
            self.simulation.input['humidity'] = test_case['humidity']
            self.simulation.input['occupancy'] = test_case['occupancy']
            self.simulation.compute()
            result_value = self.simulation.output['ac_power']

            self.variables['ac_power'].view(sim=self.simulation)
            plt.title(f"Defuzzification (Centroid) | Result: {result_value:.2f}% \n(Inputs: T=35°C, H=85%, Occ=9)")
            plt.ylabel("Membership Degree (u)")
            plt.xlabel("AC Power (%)")
            plt.grid(True, linestyle='--', alpha=0.6)
            
            logger.info("Displaying plots. Close the plot windows to finish execution.")
            plt.show()
        except Exception as e:
            logger.error(f"Visualization error (ensure matplotlib backend is correct): {e}")

def main():
    """Main execution entry point."""
    print("Adaptive Smart Environment Controller - Simulator v2.0")
    print("-----------------------------------------------------")
    
    try:
        sim_env = SmartHomeSimulator()
        
        # Run benchmarks
        sim_env.run_benchmark()
        
        # Visualize
        sim_env.visualize_system()
        
    except KeyboardInterrupt:
        logger.info("Simulation interrupted by user.")
    except Exception as e:
        logger.critical(f"Unexpected crash: {e}")

if __name__ == "__main__":
    main()
