import math

# CONSTANTS
acceleration = 0  # m/s**2
grade_radians = 0  # radians
cd = 0.7
p = 1.2041  # kg/m^3
area = 2.1  # m^2
speed_km_h = 100  # Speed in km/h
speed_m_s = speed_km_h / 3.6  # Convert speed to m/s
cr = 0.01
drive_train_efficiency = 0.4
accessory_power = 0  # kW
fuel_air_mass_ratio = 1
k = 0.9
N = 16  # Engine speed in rev/s
V = 2 # kg/L 0% EMPTY
#V = 2 # kg/L 0% EMPTY
n = 0.45
fuel_density = 0.8253912953467768  # kg/L 0% EMPTY
#fuel_density = 0.73   # kg/L 15%
#fuel_density = 0.65   # kg/L 30%

# The engine power module
def calculate_engine_power(mass, acceleration, grade_radians, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power):
    Ptract = (mass * acceleration + mass * 9.81 * math.sin(grade_radians) + 0.5 * cd * p * area * speed_m_s**2 + mass * 9.81 * cr * math.cos(grade_radians)) * speed_m_s / 1000
    P = Ptract / drive_train_efficiency + accessory_power
    return P

# The fuel rate module
def calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n):
    FR = fuel_air_mass_ratio * (k * N * V + P / n) / 44
    return FR


# Function to run scenario test
def run_scenario_test(weight, speed_km_h):
    speed_m_s = speed_km_h / 3.6  # Convert speed to m/s

    # Calculate engine power in kW
    P = calculate_engine_power(weight, acceleration, grade_radians, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power)

    # Calculate fuel rate in g/s
    fuel_rate_g_s = calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n)

    # Convert fuel rate to L/100km
    fuel_rate_kg_s = fuel_rate_g_s / 1000
    fuel_rate_L_s = fuel_rate_kg_s / fuel_density
    fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed_km_h / 100)

    # Calculate total fuel usage over 100 km
    fuel_usage_liters = fuel_rate_L_per_100km
    return fuel_usage_liters

# Define weight classes and speeds for the scenarios
weights = {
    "Light Duty": 4500,
    "Light Duty 15% weight": 5175,
    "Light Duty 30% weight": 5850
}
speeds = [50, 70, 100]

# Run scenarios and print results
for weight_class, weight in weights.items():
    print(f"Results for {weight_class}:")
    for speed in speeds:
        fuel_usage_liters = run_scenario_test(weight, speed)
        print(f"Fuel usage at {speed} km/h over 100 km: {fuel_usage_liters:} liters")
    print()

