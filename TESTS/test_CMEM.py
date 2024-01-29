import unittest
from CMEM import calculate_engine_power, calculate_fuel_rate, calculate_fuel_rates_for_speeds

class TestCMEMModel(unittest.TestCase):

    # CONSTANTS
    def setUp(self):
        self.air_density = 1.2041  # kg/m^3
        self.drag_coefficient = 0.7
        self.rolling_resistance_coefficient = 0.01
        self.drive_train_efficiency = 0.4
        self.engine_efficiency = 0.45
        self.accessory_power = 0  # hp, converted to kW
        self.area = 2.1  # m^2, small
        self.engine_friction_factor = 0.9  # kJ/rev/L, converted to kW
        self.engine_displacement = 5  # L, average of 2 and 8
        self.fuel_air_mass_ratio = 1  # Like in paper
        self.fuel_density = 0.832
        self.N = 16  # Engine speed in rev/s

    def test_flat_no_acceleration(self):
        # Test with no grade, no acceleration
        mass = 3500
        velocity_kmh = 50
        velocity_m_s = velocity_kmh / 3.6  # Convert to m/s
        grade_radians = 0

        expected_power = 17.849659609696502
        calculated_power = calculate_engine_power(mass, grade_radians, self.drag_coefficient, self.air_density, self.area, velocity_m_s, 0, self.rolling_resistance_coefficient, self.drive_train_efficiency, self.accessory_power)

        self.assertAlmostEqual(calculated_power, expected_power, places=2)

    def run_scenario_test(self, weight, speed, distance):
        # Convert speed from km/h to m/s
        speed_m_s = speed / 3.6

        # Calculate engine power
        engine_power = calculate_engine_power(weight, 0, self.drag_coefficient, self.air_density, self.area, speed_m_s, 0, self.rolling_resistance_coefficient, self.drive_train_efficiency, self.accessory_power)

        # Calculate fuel rate in g/s
        fuel_rate_g_s = calculate_fuel_rate(self.fuel_air_mass_ratio, self.engine_friction_factor, self.engine_displacement, engine_power, self.engine_efficiency)

        # Convert fuel rate to L/100km
        fuel_rate_kg_s = fuel_rate_g_s / 1000
        fuel_rate_L_s = fuel_rate_kg_s / self.fuel_density
        fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed / 100)

        return fuel_rate_L_per_100km

    def test_fuel_usage_scenarios(self):
        weights = {
            "Light Duty": 3500,
            "Medium Duty": 5000,
            "Heavy Duty": 15000
        }
        speeds = [50, 70, 100]
        distance = 100

        for weight_class, weight in weights.items():
            for speed in speeds:
                with self.subTest(weight_class=weight_class, speed=speed):
                    fuel_usage_liters = self.run_scenario_test(weight, speed, distance)
                    print(f"Fuel usage for {weight_class} at {speed} km/h over {distance} km: {fuel_usage_liters} liters")

if __name__ == '__main__':
    unittest.main()

