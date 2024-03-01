import unittest
from MEET_full import (calculate_emissions, calculate_load_correction_factor,
                       calculate_gradient_correction_factor, calculate_total_CO2_emissions,
                       convert_CO2_to_fuel_liters, get_road_gradient_parameters, road_gradient_parameters)

class TestFuelUsageScenariosWithGradient(unittest.TestCase):

    def test_get_road_gradient_parameters_uphill(self):
        # Test for different weight classes with uphill slope range "[0,4]"
        self.assertEqual(get_road_gradient_parameters(7.5, "[0,4]"), road_gradient_parameters["Weight_<=7.5"]["[0,4]"])
        self.assertEqual(get_road_gradient_parameters(16, "[0,4]"), road_gradient_parameters["Weight_7.5_to_16"]["[0,4]"])
        self.assertEqual(get_road_gradient_parameters(32, "[0,4]"),road_gradient_parameters["Weight_16_to_32"]["[0,4]"])
        self.assertEqual(get_road_gradient_parameters(33, "[0,4]"), road_gradient_parameters["Weight_>32"]["[0,4]"])

    def test_get_road_gradient_parameters_downhill(self):
        # Test for different weight classes with downhill slope range "[-4,0]"
        self.assertEqual(get_road_gradient_parameters(7.5, "[-4,0]"), road_gradient_parameters["Weight_<=7.5"]["[-4,0]"])
        self.assertEqual(get_road_gradient_parameters(16, "[-4,0]"), road_gradient_parameters["Weight_7.5_to_16"]["[-4,0]"])
        self.assertEqual(get_road_gradient_parameters(32, "[-4,0]"), road_gradient_parameters["Weight_16_to_32"]["[-4,0]"])
        self.assertEqual(get_road_gradient_parameters(33, "[-4,0]"), road_gradient_parameters["Weight_>32"]["[-4,0]"])

    def run_scenario_test(self, weight, speed, distance, gradient_percentage, slope_range):
        # Retrieve and print the road gradient parameters for the current scenario
        '''road_gradient_params = get_road_gradient_parameters(weight, slope_range)
        print(
            f"Using road gradient parameters for weight {weight} and slope range {slope_range}: {road_gradient_params}")'''
        # Calculate and print the emissions rate
        emissions_rate = calculate_emissions(weight, speed)
        '''print(f"Emissions rate for weight {weight} and speed {speed}: {emissions_rate}")'''

        # Calculate and print the load correction factor
        load_correction_factor = calculate_load_correction_factor(weight, speed, gradient_percentage)
        '''print(
            f"Load correction factor for weight {weight}, speed {speed}, and gradient_percentage {gradient_percentage}: {load_correction_factor}")'''

        # Calculate and print the gradient correction factor
        GC = calculate_gradient_correction_factor(weight, speed, slope_range)
        '''print(f"Gradient correction (GC) for weight {weight}, speed {speed}, and slope range {slope_range}: {GC}")'''

        # Calculate total emissions and print the distance
        total_emissions = calculate_total_CO2_emissions(emissions_rate, load_correction_factor, GC, distance)
        '''print(f"Total emissions for distance {distance} km: {total_emissions}")'''

        return total_emissions


    def test_fuel_usage_scenarios_with_gradient_and_load(self):
        scenarios = [
            {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[0,4]"},
            {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[-4,0]"},
            {"weight_class": "Weight_class_2", "weight": 16, "slope_range": "[0,4]"},
            {"weight_class": "Weight_class_2", "weight": 16, "slope_range": "[-4,0]"},
            {"weight_class": "Weight_class_3", "weight": 32, "slope_range": "[0,4]"},
            {"weight_class": "Weight_class_3", "weight": 32, "slope_range": "[-4,0]"},
            {"weight_class": "Weight_class_4", "weight": 33, "slope_range": "[0,4]"},
            {"weight_class": "Weight_class_4", "weight": 33, "slope_range": "[-4,0]"},
        ]
        speeds = [50, 70]
        distance = 100
        gradient_percentage = 0.15  # Example load percentages

        for scenario in scenarios:
            for speed in speeds:
                with self.subTest(weight_class=scenario["weight_class"], speed=speed,
                                  slope_range=scenario["slope_range"]):
                    total_emissions = self.run_scenario_test(scenario["weight"], speed, distance, gradient_percentage,
                                                             scenario["slope_range"])
                    fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
                    print(
                        f"{scenario['weight_class']} at {speed} km/h over {distance} km and gradient {scenario['slope_range']}: {fuel_usage_liters} liters")


if __name__ == '__main__':
    unittest.main()


