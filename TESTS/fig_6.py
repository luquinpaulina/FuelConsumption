import MEET_simple as meet_simple
import MEET_load_correction as meet_load


def compare_meet_models(weights, speeds, distance, gradient_percentage=0.15):
    results_comparison = {}

    for label, weight in weights.items():
        weight_results = {}
        for speed in speeds:
            # Calculate fuel usage for MEET simple
            emissions_rate_simple = meet_simple.calculate_emissions(weight, speed)
            total_emissions_simple = meet_simple.calculate_total_CO2_emissions(emissions_rate_simple, distance)
            fuel_usage_simple = meet_simple.convert_CO2_to_fuel_liters(total_emissions_simple)

            # Calculate fuel usage with MEET load correction
            load_correction_factor = meet_load.calculate_load_correction_factor(weight, speed, gradient_percentage)
            total_emissions_load = meet_load.calculate_total_CO2_emissions(emissions_rate_simple,
                                                                           load_correction_factor, distance)
            fuel_usage_load = meet_load.convert_CO2_to_fuel_liters(total_emissions_load)

            # Calculate percentage change
            percentage_change = ((fuel_usage_load - fuel_usage_simple) / fuel_usage_simple) * 100

            # Store results
            weight_results[speed] = {
                'fuel_usage_simple': fuel_usage_simple,
                'fuel_usage_load': fuel_usage_load,
                'percentage_change': percentage_change
            }

        results_comparison[label] = weight_results

    return results_comparison


# Example usage
weights = {
    "Weight 3.5 to 7.5 tons": 7.5,
    "Weight 7.5 to 16 tons": 16,
    "Weight 16 to 32 tons": 32,
    "Weight above 32 tons": 33,
}
speeds = list(range(30, 121, 10))
distance = 100

results_comparison = compare_meet_models(weights, speeds, distance)
print(results_comparison)

import matplotlib.pyplot as plt
import numpy as np

def plot_fuel_usage_comparison_for_weight(results_comparison, weight_label, speeds):
    # Extract the specific results for the given weight label
    weight_results = results_comparison[weight_label]

    # Prepare data for plotting
    speeds_list = speeds
    fuel_usage_simple_list = [weight_results[speed]['fuel_usage_simple'] for speed in speeds_list]
    fuel_usage_load_list = [weight_results[speed]['fuel_usage_load'] for speed in speeds_list]
    percentage_changes = [weight_results[speed]['percentage_change'] for speed in speeds_list]

    # Set up the plot
    plt.figure(figsize=(14, 8))
    bar_width = 0.35  # Width of the bars
    index = np.arange(len(speeds_list))

    # Colors and labels
    colors = ['slateblue', 'darkgrey']
    labels = ['Without Load Correction', 'With Load Correction']

    # Plotting both bars for simple and load correction
    plt.bar(index, fuel_usage_simple_list, bar_width, color=colors[0], label=labels[0])
    plt.bar(index + bar_width, fuel_usage_load_list, bar_width, color=colors[1], label=labels[1])

    # Adding percentage change text above bars
    for idx, (simple, load, change) in enumerate(zip(fuel_usage_simple_list, fuel_usage_load_list, percentage_changes)):
        height = max(simple, load)
        plt.text(idx + bar_width / 2, height + 1, f'{change:.1f}%', ha='center', va='bottom')

    # Adding details to the plot
    plt.xlabel('Speed (km/h)', fontweight='bold')
    plt.ylabel('Fuel Usage (L) for 100km distance', fontweight='bold')
    plt.xticks(index + bar_width / 2, speeds_list)
    plt.title(f'Impact of Load Correction Across Speeds: {weight_label}')
    plt.legend()
    plt.ylim(0, 40)  # Ensure y-axis starts at 0 and has a fixed upper limit for comparison
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Show the plot
    plt.show()

# Assuming results_comparison is a dictionary containing the results
weights = {
    "Weight 3.5 to 7.5 tons": 7.5,
    "Weight 7.5 to 16 tons": 16,
    "Weight 16 to 32 tons": 32,
    "Weight above 32 tons": 33,
}
speeds = list(range(30, 121, 10))  # Define the range of speeds
distance = 100  # Define the distance

# Call the function with the desired weight category
plot_fuel_usage_comparison_for_weight(results_comparison, "Weight 3.5 to 7.5 tons", speeds)



