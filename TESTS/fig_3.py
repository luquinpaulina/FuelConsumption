import MEET_simple as meet_simple
import MEET_load_correction as meet_load
import matplotlib.pyplot as plt


def compare_meet_models(weights, speeds, distance, gradient_percentage=0.15):
    # Placeholder for results
    results_comparison = {}

    for label, weight in weights.items():
        results_comparison[label] = []
        for speed in speeds:
            # Calculate fuel usage MEET simple
            emissions_rate_simple = meet_simple.calculate_emissions(weight, speed)
            total_emissions_simple = meet_simple.calculate_total_CO2_emissions(emissions_rate_simple, distance)
            fuel_usage_simple = meet_simple.convert_CO2_to_fuel_liters(total_emissions_simple)

            # Calculate fuel usage with MEET load
            load_correction_factor = meet_load.calculate_load_correction_factor(weight, speed, gradient_percentage)
            total_emissions_load = meet_load.calculate_total_CO2_emissions(emissions_rate_simple,
                                                                           load_correction_factor, distance)
            fuel_usage_load = meet_load.convert_CO2_to_fuel_liters(total_emissions_load)

            # Calculate percentage change
            percentage_change = ((fuel_usage_load - fuel_usage_simple) / fuel_usage_simple) * 100
            results_comparison[label].append((speed, percentage_change))

    # Print results
    for label, changes in results_comparison.items():
        print(f"\n{label}:")
        for speed, change in changes:
            print(f"Speed: {speed} km/h, Gradient: {gradient_percentage}, Percentage Change: {change:.2f}%")

    return results_comparison

def plot_impact_of_load_correction(weights, speeds, distance, gradient_percentage=0.15):
    results_comparison = compare_meet_models(weights, speeds, distance, gradient_percentage)

    plt.figure(figsize=(14, 6))

    # Manually define a color palette
    colors = ["navy", "royalblue", "green", "gray"]

    # Initialize a variable to keep track of the bottom of the stacked area
    bottom = [0] * len(speeds)

    # Iterate through each weight category in the results
    for i, (label, changes) in enumerate(results_comparison.items()):
        speeds, percentage_changes = zip(*changes)  # Unpack speeds and changes
        color = colors[i % len(colors)]  # Cycle through colors
        plt.fill_between(speeds, bottom, percentage_changes, color=color, label=label, alpha=0.5)
        plt.plot(speeds, percentage_changes, marker=',', linestyle='-', linewidth=1, color=color)  # Add line plot on top
        bottom = percentage_changes  # Update the bottom for the next layer

    plt.title('Impact of Load Correction Across Speeds')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Percentage Change in Fuel Usage (%)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc='upper left', fontsize=12, title="Vehicle Weight Category")
    plt.tight_layout()
    plt.ylim(0, 100)
    plt.show()

# Example usage
weights = {
    "Weight 3.5 to 7.5 tons": 7.5,
    "Weight 7.5 to 16 tons": 16,
    "Weight 16 to 32 tons": 32,
    "Weight above 32 tons": 33,
}
speeds = list(range(30, 121, 10))
distance = 100

plot_impact_of_load_correction(weights, speeds, distance)












