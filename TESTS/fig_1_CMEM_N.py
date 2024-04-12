# Import necessary libraries

from CMEM_full import *

import matplotlib.pyplot as plt


def plot_speed_vs_fuel_usage_CMEM_dynamic_N(weights, speeds, grade_degrees):
    plt.figure(figsize=(10, 6))  # Define figure size for better visibility

    for weight_label, weight in weights.items():
        fuel_usage_list = []
        engine_speed_list = []
        for speed in speeds:
            # Dynamically calculate engine speed for each speed
            N = calculate_engine_speed_Nt_rev_s(speed)  # Assume S and R_L are defined within the function or globally
            # Calculate fuel usage based on the CMEM model calculations for each speed
            fuel_usage_liters, _ = run_scenario_test(weight, speed, grade_degrees[0])  # Modified to receive dynamic N
            fuel_usage_list.append(fuel_usage_liters)
            engine_speed_list.append(N)

        # Plot the results
        plt.plot(speeds, fuel_usage_list, marker='o', linestyle='-', label=f'Weight: {weight_label} kg')

    # Customize the plot with title, labels, legend, and grid
    plt.title('Speed vs. Fuel Usage (CMEM) for Different Loads', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (Liters per 100 km)', fontsize=14)
    plt.xticks(speeds)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(title="Vehicle Weight")
    plt.tight_layout()  # Adjust layout for better fit of elements
    plt.show()

# Parameters for plotting with dynamic N
weights_focused = {
    "4500 kg": 4500,
    "4500 kg + 15% load": 5175,  # Adjusted weight labels for clarity
    "4500 kg + 30% load": 5850
}
speeds = list(range(30, 121, 10))  # Expanding speed range for sensitivity analysis
grades_degrees = [0]  # Using a single gradient for simplicity

# Execute the plotting function with specified parameters
plot_speed_vs_fuel_usage_CMEM_dynamic_N(weights_focused, speeds, grades_degrees)
