import matplotlib.pyplot as plt
from CMEM_fig_1 import *
import numpy as np


def plot_speed_vs_fuel_usage_CMEM_bar_chart(vehicle_params, speeds, grade_degrees):
    plt.figure(figsize=(14, 8))  # Adjust figure size for better visibility

    # Manually define a color palette
    colors = ['#005293', '#98c6ea', '#6B8E23', '#999999']  # Corrected palette with distinct and valid blues

    n_groups = len(speeds)
    n_bars = len(vehicle_params)
    bar_width = 0.15  # Width of a single bar
    index = np.arange(n_groups) * (n_bars * bar_width + 0.1)  # Spacing between groups

    # Loop through each set of vehicle parameters
    for i, (label, params) in enumerate(vehicle_params.items()):
        fuel_usage_list = []
        for speed in speeds:
            # Call the CMEM model function with the specified parameters
            fuel_usage_liters = run_scenario_test(params['weight'], speed, grade_degrees[0], params['area'])
            fuel_usage_list.append(fuel_usage_liters)

        # Plot the results for each load percentage at each speed
        plt.bar(index + i * bar_width, fuel_usage_list, bar_width, label=label, color=colors[i % len(colors)])

    # Customize the plot
    plt.title('Fuel Consumption Across Speeds for Different Loads - MEET', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (Liters per 100 km)', fontsize=14)
    plt.xticks(index + bar_width * (n_bars / 2 - 0.5), speeds)  # Center x-ticks between bars
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(0, 40)  # Adjust y-axis as needed
    plt.tight_layout()
    plt.show()


# Parameters for plotting, now including weight and frontal area for different load percentages
vehicle_params = {
    "Load percentage 0%": {"weight": 4500, "area": 2.1},
    "Load percentage 15%": {"weight": 5175, "area": 2.1},
    "Load percentage 30%": {"weight": 5850, "area": 2.1},
    "Load percentage 50%": {"weight": 6750, "area": 2.1},
}

speeds = list(range(20, 121, 10))
grades_degrees = [0]  # Using a single gradient for simplicity in this example

# Execute the plotting function with the specified parameters
plot_speed_vs_fuel_usage_CMEM_bar_chart(vehicle_params, speeds, grades_degrees)
