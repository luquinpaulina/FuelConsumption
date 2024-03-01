import MEET_load_correction as meet_load
import MEET_full as meet_full
import matplotlib.pyplot as plt
import numpy as np

def compare_meet_models(weights, speeds, distance, gradient_percentage, slope_range=None):
    results_comparison = {}

    for label, weight in weights.items():
        results_comparison[label] = []
        for speed in speeds:
            # Calculate fuel usage with MEET load
            emissions_rate_load = meet_load.calculate_emissions(weight, speed)
            load_correction_factor = meet_load.calculate_load_correction_factor(weight, speed, gradient_percentage)
            total_emissions_load = meet_load.calculate_total_CO2_emissions(emissions_rate_load, load_correction_factor, distance)
            fuel_usage_load = meet_load.convert_CO2_to_fuel_liters(total_emissions_load)

            if slope_range:
                # Calculate fuel usage with MEET full, considering slope_range only for the gradient correction
                GC = meet_full.calculate_gradient_correction_factor(weight, speed, slope_range)
            else:
                # Assume no slope correction if slope_range is not provided
                GC = 1  # No correction

            emissions_rate_full = meet_full.calculate_emissions(weight, speed)
            load_correction_factor_full = meet_full.calculate_load_correction_factor(weight, speed, gradient_percentage)
            total_emissions_full = meet_full.calculate_total_CO2_emissions(emissions_rate_full, load_correction_factor_full, GC, distance)
            fuel_usage_full = meet_full.convert_CO2_to_fuel_liters(total_emissions_full)

            # Calculate percentage change
            percentage_change = ((fuel_usage_full - fuel_usage_load) / fuel_usage_load) * 100 if slope_range else ((fuel_usage_load - fuel_usage_full) / fuel_usage_full) * 100
            results_comparison[label].append((speed, percentage_change))

    # Print results
    for label, changes in results_comparison.items():
        print(f"\n{label}:")
        for speed, change in changes:
            slope_info = f", Slope Range: {slope_range}" if slope_range else ""
            print(f"Speed: {speed} km/h, Gradient: {gradient_percentage*100}%{slope_info}, Percentage Change: {change:.2f}%")

    return results_comparison

def plot_impact_of_load_correction(weights, speeds, distance, gradient_percentage, slope_range=None):
    results_comparison = compare_meet_models(weights, speeds, distance, gradient_percentage, slope_range)

    plt.figure(figsize=(14, 6))
    colors = ["navy", "royalblue", "green", "gray"]

    for i, (label, changes) in enumerate(results_comparison.items()):
        speeds, percentage_changes = zip(*changes)
        color = colors[i % len(colors)]
        plt.plot(speeds, percentage_changes, marker='o', linestyle='-', linewidth=2, color=color, label=label)

    plot_title = 'Impact of Slope Correction Across Speeds' if slope_range else 'Impact of Load Correction Across Speeds'
    plt.title(plot_title)
    plt.xlabel('Speed (km/h)')
    plt.ylabel('Percentage Change in Fuel Usage (%)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(speeds, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(loc='upper left', fontsize=12, title="Vehicle Weight Category")
    plt.tight_layout()
    plt.ylim(0, 150)  # Adjusted y-limit for visibility of negative changes as well
    plt.show()

# Example usage
weights = {
    "Weight 3.5 to 7.5 tons": 7.5,
    "Weight 7.5 to 16 tons": 16,
    "Weight 16 to 32 tons": 32,
    "Weight above 32 tons": 33,
}
speeds = list(range(30, 80, 5))
distance = 100
gradient_percentage = 0.15
slope_range = "[0,4]"  # Assuming this is the correct format for your slope_range variable


# Example usage with slope_range
plot_impact_of_load_correction(weights, speeds, distance, gradient_percentage, "[0,4]")



