# test_MEET_simple.py
import unittest
from MEET_simple import get_emission_parameters, emission_parameters, calculate_emissions, calculate_total_CO2_emissions, convert_CO2_to_fuel_liters

class TestMEETModel(unittest.TestCase):

    def test_get_emission_parameters(self):
        # Test for different weight classes
        self.assertEqual(get_emission_parameters(7.5), emission_parameters["3.5_to_7.5"])
        self.assertEqual(get_emission_parameters(16), emission_parameters["7.5_to_16"])
        self.assertEqual(get_emission_parameters(32), emission_parameters["16_to_32"])
        self.assertEqual(get_emission_parameters(33), emission_parameters["above_32"])

    def test_calculate_emissions(self):
        # Test for known values
        self.assertAlmostEqual(calculate_emissions(7.5, 50), 330.915, places=2)

    def test_total_CO2_emissions(self):
        weight = 7.5  # Example weight
        speed = 50  # Example speed 50 km/h
        distance = 100  # Example distance 100 km

        emissions_rate = calculate_emissions(weight, speed)
        total_emissions = calculate_total_CO2_emissions(emissions_rate, distance)

        expected_total_emissions = emissions_rate * distance  # Calculate expected value
        self.assertAlmostEqual(total_emissions, expected_total_emissions, places=2)


    def run_scenario_test(self, weight, speed, distance):
        emissions_rate = calculate_emissions(weight, speed)
        total_emissions = calculate_total_CO2_emissions(emissions_rate, distance)
        expected_total_emissions = emissions_rate * distance
        self.assertAlmostEqual(total_emissions, expected_total_emissions, places=2)
        return expected_total_emissions

    def test_scenarios(self):
        weights = {
            "Weight_class_1": 7.5,  # Assuming within 3.5 < Weight ≤ 7.5 class
            "Weight_class_2": 16,  # Assuming within 7.5 < Weight ≤ 16 class
            "Weight_class_3": 32,  # Assuming within 16 < Weight ≤ 32 class
            "Weight_class_4": 33,  # Assuming < 32 class
        }
        speeds = [50, 70, 100]  # Speeds in km/h
        distance = 100  # Distance in km

        for weight_class, weight in weights.items():
            for speed in speeds:
                with self.subTest(weight_class=weight_class, speed=speed):
                    total_emissions = self.run_scenario_test(weight, speed, distance)
                    #print(f"Total CO2 emissions for {weight_class} at {speed} km/h over {distance} km: {total_emissions} grams")

    def test_fuel_usage_scenarios(self):
        weights = {
            "Weight_class_1": 7.5,
            "Weight_class_2": 16,
            "Weight_class_3": 32,
            "Weight_class_4": 33,
        }
        speeds = [50, 70, 100]
        distance = 100

        for weight_class, weight in weights.items():
            for speed in speeds:
                with self.subTest(weight_class=weight_class, speed=speed):
                    total_emissions = self.run_scenario_test(weight, speed, distance)
                    fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
                    print(
                        f"Fuel usage for {weight_class} at {speed} km/h over {distance} km: {fuel_usage_liters} liters")

if __name__ == '__main__':
    unittest.main()

