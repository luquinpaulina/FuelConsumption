import unittest
from MEET_load_correction import (calculate_emissions, calculate_total_CO2_emissions, convert_CO2_to_fuel_liters, calculate_load_correction_factor)

class TestMEETModel(unittest.TestCase):

    def run_scenario_test(self, weight, speed, distance, gradient_percentage):
        # Placeholder for load correction factor calculation
        # Assume calculate_load_correction_factor returns a multiplier based on gradient_percentage
        load_correction_factor = calculate_load_correction_factor(weight, speed, gradient_percentage)

        emissions_rate = calculate_emissions(weight, speed)
        # Adjust the total emissions calculation to include the load correction factor
        total_emissions = calculate_total_CO2_emissions(emissions_rate, load_correction_factor, distance)
        return total_emissions

    def test_fuel_usage_scenarios_with_load(self):
        weights = {
            "Weight_class_1": 7.5,
            "Weight_class_2": 16,
            "Weight_class_3": 32,
            "Weight_class_4": 33,
        }
        speeds = [50, 70, 100]
        distance = 100
        gradient_percentages = [0.15, 0.30]  # Example load percentages

        for weight_class, weight in weights.items():
            for speed in speeds:
                for gradient_percentage in gradient_percentages:
                    with self.subTest(weight_class=weight_class, speed=speed, gradient_percentage=gradient_percentage):
                        total_emissions = self.run_scenario_test(weight, speed, distance, gradient_percentage)
                        fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
                        print(
                            f"Fuel usage for {weight_class} at {speed} km/h over {distance} km with load {gradient_percentage*100}%: {fuel_usage_liters} liters")

if __name__ == '__main__':
    unittest.main()
