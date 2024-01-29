import math
import matplotlib.pyplot as plt

# The engine power module
def calculate_engine_power(mass, grade_radians, drag_coefficient, air_density, area, velocity, acceleration, rolling_resistance_coefficient, drive_train_efficiency, accessory_power):
    # Convert grade from degrees to radians for the sin function
    #grade_radians = math.radians(grade)


    # Adjusted tractive power requirements (Ptract) in kW, including acceleration
    Ptract = (mass * acceleration + mass * 9.81 * math.sin(grade_radians) + 0.5 * drag_coefficient * air_density * area * velocity**2 + mass * 9.81 * rolling_resistance_coefficient) * velocity / 1000

    # Total engine power (P) in kW
    P = Ptract / drive_train_efficiency + accessory_power
    return P

# The engine speed module
# N engine speed (rev/s) 16–48
N = 16 # THIS WE ARE NOT SURE

# The fuel consumption model
def calculate_fuel_rate(fuel_air_mass_ratio, engine_friction_factor, engine_displacement, engine_power, engine_efficiency):
    # Fuel rate (FR) in g/s
    FR = fuel_air_mass_ratio * (engine_friction_factor * N * engine_displacement + engine_power / engine_efficiency) / 44
    return FR

# Constants
air_density = 1.2041  # kg/m^3
drag_coefficient = 0.7
rolling_resistance_coefficient = 0.01
drive_train_efficiency = 0.4
engine_efficiency = 0.45
accessory_power = 0  # hp, converted to kW
#frontal_area = 3.85  # m^2, average of 2.1 and 5.6
area = 2.1  # m^2, small # THIS WE ARE NOT SURE 2.1–5.6
#frontal_area = 5.6  # m^2, big
engine_friction_factor = 0.9  # kJ/rev/L, converted to kW
engine_displacement = 2  # L,  2–8 # THIS WE ARE NOT SURE
fuel_air_mass_ratio =1  # Like in paper
acceleration = 0 # THIS WE ARE NOT SURE
grade_radians = 0  # THIS WE ARE NOT SURE


def calculate_fuel_rates_for_speeds(weight, min_speed, max_speed, step):
    results = {}
    fuel_density = 0.832  # Density of diesel fuel in kg/L
    for speed_kmh in range(min_speed, max_speed + 1, step):
        speed_m_s = speed_kmh / 3.6  # Convert speed from km/h to m/s

        # Calculate engine power and fuel rate
        engine_power = calculate_engine_power(weight, 0, drag_coefficient, air_density, area, speed_m_s, 0, rolling_resistance_coefficient, drive_train_efficiency, accessory_power)
        fuel_rate_g_s = calculate_fuel_rate(fuel_air_mass_ratio, engine_friction_factor, engine_displacement, engine_power, engine_efficiency)

        # Convert fuel rate to kg/s (assuming diesel fuel density)
        fuel_rate_kg_s = fuel_rate_g_s / 1000

        # Convert fuel rate to L/s using fuel density
        fuel_rate_L_s = fuel_rate_kg_s / fuel_density

        # Convert fuel rate to L/100km
        fuel_rate_L_per_100km = fuel_rate_L_s * 3600 / (speed_kmh / 100)

        results[speed_kmh] = fuel_rate_L_per_100km

    return results



light_duty_weight = 3500  # kg, maximum weight for light duty vehicle
medium_duty_weight = 5000  # kg, example weight for medium duty vehicle (assumed)
heavy_duty_weight = 32000  # kg, minimum weight for heavy duty vehicle


# Run simulation for each vehicle type
light_duty_results = calculate_fuel_rates_for_speeds(light_duty_weight, 20, 200, 10)
medium_duty_results = calculate_fuel_rates_for_speeds(medium_duty_weight, 20, 200, 10)
heavy_duty_results = calculate_fuel_rates_for_speeds(heavy_duty_weight, 20, 200, 10)


# Plotting function
def plot_fuel_rates(vehicle_results, title):
    plt.figure(figsize=(10, 6))
    for vehicle_type, results in vehicle_results.items():
        speeds = list(results.keys())
        fuel_rates = list(results.values())
        plt.plot(speeds, fuel_rates, marker='o', label=vehicle_type)

    plt.title(title)
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Consumption (L/100km)')
    plt.xticks(range(20, 200, 10))
    plt.legend()
    plt.grid(True)
    plt.show()

# Plotting for all vehicle types
plot_fuel_rates({'Light Duty': light_duty_results, 'Medium Duty': medium_duty_results, 'Heavy Duty': heavy_duty_results}, 'Fuel Consumption vs Speed for Different Vehicle Types')
