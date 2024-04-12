import MEET_load_correction as meet_load
import matplotlib.pyplot as plt
import numpy as np

def calculate_fuel_consumption_meet_load(weight, speeds, distance, gradient_percentages, zero_percent_load_results=None):
    # Placeholder for fuel consumption results specifically for MEET load across different gradient percentages
    fuel_consumption_results = {}

    # Check and add 0% load results if provided
    if zero_percent_load_results is not None and 0 in gradient_percentages:
        fuel_consumption_results[0] = zero_percent_load_results

    for gradient_percentage in gradient_percentages:
        if gradient_percentage == 0 and zero_percent_load_results is not None:
            continue  # Skip calculation for 0% if results are already provided
        fuel_consumptions = []

        for speed in speeds:
            # Calculate fuel usage with MEET load
            load_correction_factor = meet_load.calculate_load_correction_factor(weight, speed, gradient_percentage)
            emissions_rate_simple = meet_load.calculate_emissions(weight, speed)
            total_emissions_load = meet_load.calculate_total_CO2_emissions(emissions_rate_simple,
                                                                           load_correction_factor, distance)
            fuel_usage_load = meet_load.convert_CO2_to_fuel_liters(total_emissions_load)

            fuel_consumptions.append(fuel_usage_load)

        fuel_consumption_results[gradient_percentage] = fuel_consumptions

    return fuel_consumption_results, speeds

def plot_fuel_consumption_by_gradient(weight, speeds, distance, gradient_percentages, zero_percent_load_results=None):
    fuel_consumption_results, speeds = calculate_fuel_consumption_meet_load(weight, speeds, distance,
                                                                            gradient_percentages, zero_percent_load_results)
    # Print results
    for gp in sorted(gradient_percentages):
        print(f"\nGradient: {gp * 100}%:")
        for i, speed in enumerate(speeds):
            print(f"Speed: {speed} km/h, Fuel Usage: {fuel_consumption_results[gp][i]:.2f} L/100km")

    # Set up the plot
    plt.figure(figsize=(14, 8))

    colors = ['#005293', '#98c6ea', '#6B8E23', '#999999']  # Adjusted color palette
    labels = [f"Load percentage: {gp * 100}%" for gp in gradient_percentages]

    # Plot each gradient as a separate line
    for i, gp in enumerate(sorted(gradient_percentages)):
        plt.plot(speeds, fuel_consumption_results[gp], color=colors[i % len(colors)], label=labels[i], marker='o', linestyle='-')

    plt.title('Fuel Consumption Across Speeds for Different Loads')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Usage (L) for 100km distance')
    plt.xticks(speeds)
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Parameters
weight = 4.5  # Single weight category
speeds = list(range(20, 121, 10))
distance = 100
zero_percent_load_results = [
    17.143125234580257,
    12.829715584469744,
    10.995558613787065,
    10.350150131364945,
    10.510238125026063,
    11.351785490875944,
    12.847960715626174,
    15.015134770702144,
    17.89127986988615,
    21.526150722791535,
    25.976375161599737
]
gradient_percentages = [0, 0.15, 0.3, 0.5]

# Function call
plot_fuel_consumption_by_gradient(weight, speeds, distance, gradient_percentages, zero_percent_load_results)
