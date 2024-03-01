import MEET_load_correction as meet_load
import matplotlib.pyplot as plt
import numpy as np

def calculate_fuel_consumption_meet_load(weight, speeds, distance, gradient_percentages):
    # Placeholder for fuel consumption results specifically for MEET load across different gradient percentages
    fuel_consumption_results = {}

    for gradient_percentage in gradient_percentages:
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


def plot_fuel_consumption_by_gradient(weight, speeds, distance, gradient_percentages):
    fuel_consumption_results, speeds = calculate_fuel_consumption_meet_load(weight, speeds, distance,
                                                                            gradient_percentages)
    # Print results
    for gp in sorted(gradient_percentages):
        print(f"\nGradient: {gp * 100}%:")
        for i, speed in enumerate(speeds):
            print(f"Speed: {speed} km/h, Fuel Usage: {fuel_consumption_results[gp][i]:.2f} L/100km")

    # Set up the plot
    plt.figure(figsize=(14, 8))

    # Number of groups and number of bars in each group
    n_groups = len(speeds)
    n_bars = len(gradient_percentages)

    # Calculate the width of each bar
    bar_width = 0.8 / n_bars  # Dynamic width to accommodate all bars
    index = np.arange(n_groups)

    colors = ['slateblue', 'darkgrey', 'darkseagreen']
    labels = [f"Load percentage: {gp * 100}%" for gp in gradient_percentages]

    for i, gp in enumerate(sorted(gradient_percentages)):
        fuel_consumptions = fuel_consumption_results[gp]
        # Position of each bar on the x-axis
        bar_positions = index + i * bar_width

        plt.bar(bar_positions, fuel_consumptions, bar_width, color=colors[i % len(colors)], label=labels[i])

    plt.title('Fuel Consumption Across Speeds for Different Loads')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Fuel Usage (L) for 100km distance')
    plt.xticks(index + bar_width / 2 * (n_bars - 1), [f"{speed} km/h" for speed in speeds])
    plt.legend(loc='upper left')
    plt.ylim(0, 60)  # Set y-axis to range from 5 to 60 liters
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()


# Parameters
weight = 32  # Single weight category
speeds = list(range(30, 121, 10))
distance = 100
gradient_percentages = [0.15, 0.3, 0.5]

# Function call
plot_fuel_consumption_by_gradient(weight, speeds, distance, gradient_percentages)
