import math

# Constants
acceleration = 0  # m/s^2
cd = 0.7
p = 1.2041  # Air density (kg/m^3)
cr = 0.01  # Coefficient of rolling resistance
drive_train_efficiency = 0.4
accessory_power = 0  # kW
fuel_air_mass_ratio = 1
k = 0.9
N = 16  # Engine speed (rev/s)
V = 2  # Engine displacement (L)
n = 0.45
fuel_density = 0.8253912953467768  # Fuel density (kg/L)

# Adjusted to accept `area` as a parameter
def calculate_engine_power(mass, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power):
    grade_radians = math.radians(grade_degrees)  # Convert grade from degrees to radians
    Ptract = (mass * acceleration + mass * 9.81 * math.sin(grade_radians) + 0.5 * cd * p * area * speed_m_s**2 + mass * 9.81 * cr * math.cos(grade_radians)) * speed_m_s / 1000
    P = Ptract / drive_train_efficiency + accessory_power
    return P

def calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n):
    FR = fuel_air_mass_ratio * (k * N * V + P / n) / 44
    return FR

# Now accepts `area` parameter
def run_scenario_test(weight, speed_km_h, grade_degrees, area):
    speed_m_s = speed_km_h / 3.6  # Convert speed to m/s

    P = calculate_engine_power(weight, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power)

    fuel_rate_g_s = calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n)

    fuel_rate_kg_s = fuel_rate_g_s / 1000
    fuel_rate_L_s = fuel_rate_kg_s / fuel_density
    fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed_km_h / 100)

    fuel_usage_liters = fuel_rate_L_per_100km
    return fuel_usage_liters
