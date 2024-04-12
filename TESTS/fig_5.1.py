import matplotlib.pyplot as plt
import numpy as np
import MEET_gradient as meet_gradient

def calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results=None):
    bar_width = 0.1  # Width of each bar
    n_scenarios = len(scenarios) + (1 if zero_gradient_results else 0)  # Including zero gradient scenario

    index = np.arange(len(speeds))  # Index for speeds

    plt.figure(figsize=(14, 8))

    # If zero gradient results are provided, plot them
    if zero_gradient_results:
        pos_zero_gradient = [x - bar_width for x in index]  # Position for zero gradient bars
        plt.bar(pos_zero_gradient, zero_gradient_results, width=bar_width, label="Zero Gradient", color='grey')

    # Iterate through each scenario for other gradients
    for i, scenario in enumerate(scenarios):
        fuel_consumptions = []
        for speed in speeds:
            emissions_rate_simple = meet_gradient.calculate_emissions(scenario['weight'], speed)
            slope_range = scenario['slope_range']
            GC = meet_gradient.calculate_gradient_correction_factor(scenario['weight'], speed, slope_range)
            total_emissions_load = meet_gradient.calculate_total_CO2_emissions(emissions_rate_simple, GC, distance)
            fuel_usage_load = meet_gradient.convert_CO2_to_fuel_liters(total_emissions_load)
            fuel_consumptions.append(fuel_usage_load)

        # Calculate position for each bar in the scenario
        pos = [x + (i * bar_width) for x in index]
        plt.bar(pos, fuel_consumptions, width=bar_width, label=f"{scenario['weight_class']}, Slope: {scenario['slope_range']}")

    plt.title('Fuel Consumption Across Speeds for Different Scenarios')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Usage (L) for 100km distance')
    # Adjust x-ticks to center them for each group of bars
    plt.xticks([r + bar_width * (n_scenarios / 2 - 1) for r in range(len(speeds))], speeds)
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Parameters
speeds = list(range(20, 61, 10))
distance = 100

# Define your scenarios
scenarios = [
    {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[0,4]"},
    {"weight_class": "Weight_class_1", "weight": 7.5, "slope_range": "[-4,0]"},
]

zero_gradient_results = [17.143, 12.829, 10.995, 10.350, 10.510]  # Example zero gradient results

# Call the function with zero gradient results
calculate_and_plot_fuel_consumption_for_scenarios(scenarios, speeds, distance, zero_gradient_results)



