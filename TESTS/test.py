import matplotlib.pyplot as plt
import numpy as np
import MEET_gradient as meet_gradient


def calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results=None):
    # Define colors for the bars
    colors = ['#005293', '#98c6ea', '#6B8E23', '#999999']

    # Define the width of each bar and calculate index for bar positions
    bar_width = 0.15
    index = np.arange(len(speeds))

    plt.figure(figsize=(14, 8))

    # Plot zero gradient results first, if provided
    if zero_gradient_results is not None:
        plt.bar(index - bar_width, zero_gradient_results, width=bar_width, label="0% Slope", color=colors[0])

    # Adjust the scenarios' ordering to ensure "4% Slope" comes last
    scenarios = sorted(scenarios, key=lambda x: x['slope_range'] == "[0,4]")

    # Map slope_range to readable labels
    slope_labels = {"[-4,0]": "-4% Slope", "[0,4]": "4% Slope"}

    for i, scenario in enumerate(scenarios):
        fuel_consumptions = []
        for speed in speeds:
            emissions_rate_simple = meet_gradient.calculate_emissions(scenario['weight'], speed)
            slope_range = scenario['slope_range']
            GC = meet_gradient.calculate_gradient_correction_factor(scenario['weight'], speed, slope_range)
            total_emissions_load = meet_gradient.calculate_total_CO2_emissions(emissions_rate_simple, GC, distance)
            fuel_usage_load = meet_gradient.convert_CO2_to_fuel_liters(total_emissions_load)
            fuel_consumptions.append(fuel_usage_load)

        # Calculate the offset for bar positions based on scenario index
        pos = index + (i * bar_width) + (bar_width if zero_gradient_results is not None else 0)

        # Plotting the bars for each scenario
        plt.bar(pos, fuel_consumptions, width=bar_width, label=slope_labels.get(scenario['slope_range'], "Slope"),
                color=colors[(i + 1) % len(colors)])

    plt.title('Fuel Consumption Across Speeds for Different Slopes')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Usage (L) for 100km distance')
    plt.xticks(index + bar_width, speeds)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


# Example usage
speeds = list(range(20, 61, 10))
distance = 100
scenarios = [
    {"weight": 7.5, "slope_range": "[-4,0]"},
    {"weight": 7.5, "slope_range": "[0,4]"},
]
zero_gradient_results = [17.143, 12.829, 10.995, 10.350, 10.510]  # Example zero gradient results

# Call the function with zero gradient results
calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results)