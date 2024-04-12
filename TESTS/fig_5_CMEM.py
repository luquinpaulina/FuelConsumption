import matplotlib.pyplot as plt
import numpy as np
from CMEM_fig_1 import *  # Assuming this contains a function run_scenario_test accepting weight, speed, grade, and area.


def slope_degrees_to_percentage(slope_degrees):
    """Convert slope from degrees to percentage."""
    return np.tan(np.radians(slope_degrees)) * 100


def calculate_and_plot_fuel_consumption_for_scenarios_CMEM(scenarios, speeds, distance):
    # Define the color palette
    colors = ['#005293', '#98c6ea', '#6B8E23', '#999999']

    plt.figure(figsize=(14, 8))

    # Loop through scenarios to calculate fuel consumption
    for scenario in scenarios:
        fuel_consumptions = []
        for speed in speeds:
            fuel_usage_liters = run_scenario_test(scenario['weight'], speed, scenario['slope_degrees'],
                                                  scenario['area'])
            fuel_consumptions.append(fuel_usage_liters)

        # Convert slope degrees to percentage for legend labeling
        slope_percentage = slope_degrees_to_percentage(scenario['slope_degrees'])
        label = f"{slope_percentage:.0f}% Slope"  # Formatting to 0 decimal places

        # Plotting fuel consumption across speeds
        plt.bar(np.arange(len(speeds)) + 0.2 * list(scenarios).index(scenario), fuel_consumptions, width=0.2,
                label=label, color=colors[list(scenarios).index(scenario) % len(colors)])

    # Customizing the plot
    plt.title('Fuel Consumption Across Speeds for Different Slopes - CMEM', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (Liters per 100 km)', fontsize=14)
    plt.xticks(np.arange(len(speeds)), speeds)
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.ylim(-20, 100)  # Adjust as needed based on your data range
    plt.tight_layout()
    plt.show()


# Define vehicle parameters and gradients, expressed in degrees initially
scenarios = [
    {"weight": 4500, "area": 2.1, "slope_degrees": -2.29},  # Will be converted to ~-2% slope
    #{"weight": 4500, "area": 2.1, "slope_degrees": -1.14},  # Will be converted to ~-2% slope
    {"weight": 4500, "area": 2.1, "slope_degrees": 0},  # Will be converted to 0% slope
    #{"weight": 4500, "area": 2.1, "slope_degrees": 1.14}  # Will be converted to ~2% slope
    {"weight": 4500, "area": 2.1, "slope_degrees": 2.29}  # Will be converted to ~2% slope
]

speeds = list(range(20, 121, 10))
distance = 100  # Assuming this is used somewhere in your CMEM model

# Execute the plotting function
calculate_and_plot_fuel_consumption_for_scenarios_CMEM(scenarios, speeds, distance)


