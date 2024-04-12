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
# N = 16  # This will now be calculated dynamically
V = 2  # Engine displacement (L)
n = 0.45
fuel_density = 0.8253912953467768  # Fuel density (kg/L)

# Hypothetical values for S and R(L), you'll need to adjust these based on your vehicle
S = 33  # Example engine speed-vehicle speed ratio in top gear (rpm/mph)
R_L = 1  # Assuming we are in top gear, so gear ratio = 1

def calculate_engine_speed_Nt_rev_s(v_t_km_h, S=S, R_L=R_L):
    """
    Calculate engine speed N(t) in revolutions per second (rev/s) given vehicle speed v(t) in km/h.
    """
    v_t_mph = v_t_km_h * 0.621371  # Convert vehicle speed from km/h to mph
    N_t_rpm = S * R_L * v_t_mph  # Calculate engine speed N(t) in rpm
    N = N_t_rpm / 60  # Convert rpm to rev/s
    return N

# Adjusted functions to use dynamically calculated N
def calculate_engine_power(mass, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency, accessory_power, N):
    grade_radians = math.radians(grade_degrees)  # Convert grade from degrees to radians
    Ptract = (mass * acceleration + mass * 9.81 * math.sin(grade_radians) + 0.5 * cd * p * area * speed_m_s**2 + mass * 9.81 * cr * math.cos(grade_radians)) * speed_m_s / 1000
    P = Ptract / drive_train_efficiency + accessory_power
    return P

def calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n):
    FR = fuel_air_mass_ratio * (k * N * V + P / n) / 44
    return FR

# Running the scenarios remains the same
# Function to run scenario test, now accepting grade_degrees
# Modified run_scenario_test function to print N
def run_scenario_test(weight, speed_km_h, grade_degrees):
    speed_m_s = speed_km_h / 3.6  # Convert speed to m/s
    N = calculate_engine_speed_Nt_rev_s(speed_km_h)  # Calculate engine speed dynamically

    # Calculate engine power in kW using the dynamically calculated N
    P = calculate_engine_power(weight, acceleration, grade_degrees, cd, p, area, speed_m_s, cr, drive_train_efficiency,
                               accessory_power, N)

    # Calculate fuel rate in g/s
    fuel_rate_g_s = calculate_fuel_rate(fuel_air_mass_ratio, k, N, V, P, n)

    # Convert fuel rate to L/100km
    fuel_rate_kg_s = fuel_rate_g_s / 1000
    fuel_rate_L_s = fuel_rate_kg_s / fuel_density
    fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed_km_h / 100)

    # Calculate total fuel usage over 100 km
    fuel_usage_liters = fuel_rate_L_per_100km

    # Print the dynamically calculated N along with the fuel usage
    return fuel_usage_liters, N

# Define scenarios
grades_degrees = [0, 0.57, 1.15, -0.57, -1.15]
weights = {
    "Light Duty": 4500,
    "Light Duty 15% weight": 5175,
    "Light Duty 30% weight": 5850
}
speeds = [50, 70, 100]

# Adjusted section to run scenarios and print results including N
for grade in grades_degrees:
    print(f"Results for grade {grade} degrees:")
    for weight_class, weight in weights.items():
        print(f"  {weight_class}:")
        for speed in speeds:
            fuel_usage_liters, N = run_scenario_test(weight, speed, grade)
            print(
                f"    Speed: {speed} km/h - Engine Speed: {N:.2f} rev/s - Fuel usage over 100 km: {fuel_usage_liters:.2f} liters")
    print()
