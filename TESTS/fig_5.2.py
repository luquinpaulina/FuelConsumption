import matplotlib.pyplot as plt
import numpy as np
import MEET_gradient as meet_gradient


def calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results=None):
    # Colors for the bars
    colors = ['#005293', '#98c6ea', '#6B8E23', '#999999']  # Palette with distinct and valid colors

    # Define the width of each bar
    bar_width = 0.15

    # Sort scenarios by slope range, putting "[0,4]" last
    scenarios = sorted(scenarios, key=lambda x: x['slope_range'] == "[0,4]")

    # Create an array with the positions of the groups
    index = np.arange(len(speeds))

    plt.figure(figsize=(14, 8))

    # Additional scenarios including zero gradient results
    if zero_gradient_results:
        scenarios.insert(0, {"weight_class": "Zero Gradient", "slope_range": "0%",
                             "fuel_consumptions": zero_gradient_results})

    # Update color index outside the loop to cycle colors for each scenario
    color_index = 0

    # Plot for each scenario
    for scenario in scenarios:
        # If zero gradient, the fuel consumptions are already provided
        if 'fuel_consumptions' in scenario:
            fuel_consumptions = scenario['fuel_consumptions']
            slope_label = "0% Slope"
        else:
            fuel_consumptions = []
            for speed in speeds:
                emissions_rate_simple = meet_gradient.calculate_emissions(scenario['weight'], speed)
                slope_range = scenario['slope_range']
                GC = meet_gradient.calculate_gradient_correction_factor(scenario['weight'], speed, slope_range)
                total_emissions_load = meet_gradient.calculate_total_CO2_emissions(emissions_rate_simple, GC, distance)
                fuel_usage_load = meet_gradient.convert_CO2_to_fuel_liters(total_emissions_load)
                fuel_consumptions.append(fuel_usage_load)
            slope_label = f"{scenario['slope_range']} Slope" if scenario['slope_range'] != "0%" else "0% Slope"

        # Calculate position for each bar
        pos = [x + (color_index * bar_width) for x in index]

        # Plotting
        plt.bar(pos, fuel_consumptions, width=bar_width, label=slope_label, color=colors[color_index % len(colors)])
        color_index += 1

    plt.title('Fuel Consumption Across Speeds for Different Slopes - MEET')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Usage (L) for 100km distance')

    # Adjust x-ticks to be in the center of the group for each speed
    plt.xticks([r + bar_width for r in range(len(speeds))], speeds)

    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--', linewidth=0.5, which='both')
    plt.ylim(0, 40)  # Adjust as needed
    plt.tight_layout()
    plt.show()


# Parameters
speeds = list(range(20, 61, 10))
distance = 100

# Define your scenarios
scenarios = [
    {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[-4,0]"},
    {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[0,4]"}
]

# Example zero gradient results
zero_gradient_results = [17.143, 12.829, 10.995, 10.350, 10.510]

# Call the function with zero gradient results
calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results)
