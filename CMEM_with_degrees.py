import math

# Constants
acceleration = 0  # m/s^2
cd = 0.7
p = 1.2041  # Air density (kg/m^3)
area = 2.1  # Frontal area (m^2)
cr = 0.01  # Coefficient of rolling resistance
drive_train_efficiency = 0.4
accessory_power = 0  # kW
fuel_air_mass_ratio = 1
k = 0.9
N = 16  # Engine speed (Engine speed module) (rev/s)
V = 2  # Engine displacement (L)
n = 0.45
fuel_density = 0.8253912953467768  # Fuel density (kg/L)

# The engine power module
def calculate_engine_power(mass, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power):
    grade_radians = math.radians(grade_degrees)  # Convert grade from degrees to radians
    Ptract = (mass * acceleration + mass * 9.81 * math.sin(grade_radians) + 0.5 * cd * p * area * speed_m_s**2 + mass * 9.81 * cr * math.cos(grade_radians)) * speed_m_s / 1000
    P = Ptract / drive_train_efficiency + accessory_power
    return P

# The fuel rate module
def calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n):
    FR = fuel_air_mass_ratio * (k * N * V + P / n) / 44
    return FR

# Function to run scenario test, now accepting grade_degrees
def run_scenario_test(weight, speed_km_h, grade_degrees):
    speed_m_s = speed_km_h / 3.6  # Convert speed to m/s

    # Calculate engine power in kW
    P = calculate_engine_power(weight, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power)

    # Calculate fuel rate in g/s
    fuel_rate_g_s = calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n)

    # Convert fuel rate to L/100km
    fuel_rate_kg_s = fuel_rate_g_s / 1000
    fuel_rate_L_s = fuel_rate_kg_s / fuel_density
    fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed_km_h / 100)

    # Calculate total fuel usage over 100 km
    fuel_usage_liters = fuel_rate_L_per_100km
    return fuel_usage_liters

# Define scenarios
grades_degrees = [0, 0.57, 1.15, -0.57, -1.15]
weights = {
    "Light Duty": 4500,
    "Light Duty 15% weight": 5175,
    "Light Duty 30% weight": 5850
}
speeds = [50, 70, 100]

# Run scenarios and print results
for grade in grades_degrees:
    print(f"Results for grade {grade} degrees:")
    for weight_class, weight in weights.items():
        print(f"  {weight_class}:")
        for speed in speeds:
            fuel_usage_liters = run_scenario_test(weight, speed, grade)
            print(f"    Fuel usage at {speed} km/h over 100 km: {fuel_usage_liters:.2f} liters")
    print()
