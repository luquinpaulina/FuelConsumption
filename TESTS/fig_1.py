from MEET_simple import calculate_emissions, calculate_total_CO2_emissions, convert_CO2_to_fuel_liters
import matplotlib.pyplot as plt
import numpy as np

# Sensitivity Analysis
# Objective: Determine how sensitive the CO2 emission estimates are to changes in vehicle load and road gradient.
# Method: Vary the load and gradient parameters systematically within realistic ranges and observe the variations in CO2 emission estimates. This could help identify thresholds or nonlinearities in how these factors affect emissions.

#  1. Speed vs. Emissions/Fuel Consumption
#  Objective: Understand how varying speeds affect CO2 emissions and fuel consumption for a fixed vehicle weight.

def plot_speed_vs_fuel_usage_for_weights(weights, speeds, distance):
    plt.figure(figsize=(14, 7))  # Adjusted for better readability

    # Manually define a color palette
    colors = ["navy", "royalblue", "green", "gray"]

    for (label, weight), color in zip(weights.items(), colors):
        fuel_usage_list = []
        for speed in speeds:
            emissions_rate = calculate_emissions(weight, speed)
            total_emissions = calculate_total_CO2_emissions(emissions_rate, distance)
            fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
            fuel_usage_list.append(fuel_usage_liters)

        # Plot
        plt.plot(speeds, fuel_usage_list, marker='o', linestyle='-', linewidth=2, color=color, label=label)

    # Enhancements for a professional look
    plt.title('Speed vs Fuel Usage for Different Weight Categories - MEET', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (L) for 100km distance', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    #plt.ylim(5, 70)  # Set y-axis to range from 5 to 60 liters
    plt.ylim(0, 100)  # DEMIR
    plt.legend(loc='upper left', fontsize=12, title="Vehicle Weight Category")
    plt.tight_layout()

    # Show plot
    plt.show()

weights = {
    "Weight 3.5 to 7.5 tons": 7.5,
    "Weight 7.5 to 16 tons": 16,
    "Weight 16 to 32 tons": 32,
    "Weight above 32 tons": 33,
}
#speeds = list(range(30, 121, 10))  # Expanding speed range for sensitivity
speeds = list(range(20, 121, 10))  # DEMIR
distance = 100

plot_speed_vs_fuel_usage_for_weights(weights, speeds, distance)


def find_optimal_speed_for_min_fuel(weights, speeds, distance):
    optimal_speeds = {}
    for label, weight in weights.items():
        min_fuel_usage = float('inf')
        optimal_speed = None
        for speed in speeds:
            emissions_rate = calculate_emissions(weight, speed)
            total_emissions = calculate_total_CO2_emissions(emissions_rate, distance)
            fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
            if fuel_usage_liters < min_fuel_usage:
                min_fuel_usage = fuel_usage_liters
                optimal_speed = speed
        optimal_speeds[label] = (optimal_speed, min_fuel_usage)

    # Print the optimal speeds and corresponding minimum fuel usage for each weight category
    for label, (speed, fuel_usage) in optimal_speeds.items():
        print(
            f"{label}: Optimal speed for minimum fuel consumption is {speed} km/h with {fuel_usage:.2f} liters/100km.")


# Call the function with the defined parameters
find_optimal_speed_for_min_fuel(weights, speeds, distance)


