from MEET_load_correction import calculate_emissions, calculate_total_CO2_emissions, convert_CO2_to_fuel_liters, calculate_load_correction_factor
import matplotlib.pyplot as plt
import numpy as np


def plot_speed_vs_fuel_usage_for_weights(weights, speeds, distance, gradient_percentage):
    plt.figure(figsize=(14, 7))  # Adjusted for better readability

    # Manually define a color palette
    colors = ["navy", "royalblue", "green", "gray"]

    for (label, weight), color in zip(weights.items(), colors):
        fuel_usage_list = []
        for speed in speeds:
            emissions_rate = calculate_emissions(weight, speed)
            load_correction_factor = calculate_load_correction_factor(weight, speed, gradient_percentage)
            total_emissions = calculate_total_CO2_emissions(emissions_rate, load_correction_factor, distance)
            fuel_usage_liters = convert_CO2_to_fuel_liters(total_emissions)
            fuel_usage_list.append(fuel_usage_liters)

        # Plot
        plt.plot(speeds, fuel_usage_list, marker='o', linestyle='-', linewidth=2, color=color, label=label)

    # Enhancements for a professional look
    plt.title('Speed vs Fuel Usage for Different Weight Categories - MEET + load factor', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (L) for 100km distance', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(5, 70)  # Set y-axis to range from 5 to 60 liters
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
speeds = list(range(30, 121, 10))  # Expanding speed range for sensitivity analysis
distance = 100
gradient_percentage = 0.15

plot_speed_vs_fuel_usage_for_weights(weights, speeds, distance, gradient_percentage)