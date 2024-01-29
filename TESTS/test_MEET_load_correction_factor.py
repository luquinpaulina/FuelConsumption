import unittest
from MEET_load_correction_factor import get_emission_parameters, emission_parameters, get_load_correction_factors, \
        load_correction_factors, calculate_emissions, calculate_total_CO2_emissions, convert_CO2_to_fuel_liters, \
        calculate_load_correction_factor
class TestMEETModel(unittest.TestCase):

    def test_get_emission_parameters(self):
        # Test for different weight classes
        self.assertEqual(get_emission_parameters(7.5), emission_parameters["3.5_to_7.5"])
        self.assertEqual(get_emission_parameters(16), emission_parameters["7.5_to_16"])
        self.assertEqual(get_emission_parameters(32), emission_parameters["16_to_32"])
        self.assertEqual(get_emission_parameters(33), emission_parameters["above_32"])

    def test_get_load_correction_factors(self):
        # Test for different weight classes
        self.assertEqual(get_load_correction_factors(7.5), load_correction_factors["Weight_<=7.5"])
        self.assertEqual(get_load_correction_factors(16), load_correction_factors["Weight_7.5_to_16"])
        self.assertEqual(get_load_correction_factors(32), load_correction_factors["Weight_16_to_32"])
        self.assertEqual(get_load_correction_factors(33), load_correction_factors["Weight_>32"])

    def test_calculate_emissions(self):
        # Test for known values
        self.assertAlmostEqual(calculate_emissions(7.5, 50), 330.915, places=2)

    def test_calculate_load_correction_factor(self):
        # Test for known values
        expected_value_for_weight_7_5_speed_50 = -133.186647
        expected_value_for_weight_16_speed_50 = -131.0628000000016

        self.assertAlmostEqual(calculate_load_correction_factor(7.5, 50), expected_value_for_weight_7_5_speed_50, places=2)
        self.assertAlmostEqual(calculate_load_correction_factor(16, 50), expected_value_for_weight_16_speed_50, places=2)

if __name__ == '__main__':
    unittest.main()
