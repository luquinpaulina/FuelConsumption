import matplotlib.pyplot as plt
from CMEM_fig_1 import *


def plot_speed_vs_fuel_usage_CMEM(vehicle_params, speeds, grade_degrees):
    plt.figure(figsize=(10, 6))  # Define figure size for better visibility

    # Manually define a color palette
    colors = ["navy", "royalblue", "green", "gray"]
    color_index = 0  # Initialize color index to iterate over the colors list

    # Loop through each set of vehicle parameters
    for label, params in vehicle_params.items():
        fuel_usage_list = []
        for speed in speeds:
            # Update the run_scenario_test call to use individual parameters per vehicle
            # Assume run_scenario_test now takes `area` as an argument; adjust accordingly if different
            fuel_usage_liters = run_scenario_test(params['weight'], speed, grade_degrees[0], params['area'])
            fuel_usage_list.append(fuel_usage_liters)

        # Plot the results using the current color
        plt.plot(speeds, fuel_usage_list, marker='o', linestyle='-', label=label, color=colors[color_index])
        color_index = (color_index + 1) % len(colors)  # Update color index for the next line

    # Customize the plot with title, labels, legend, and grid
    plt.title('Speed vs Fuel Usage for Different Weight Categories - CMEM', fontsize=16)
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (Liters per 100 km)', fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    #plt.xticks(speeds)
    plt.ylim(0, 100)  # DEMIR
    plt.legend(loc='upper left', fontsize=12, title="Vehicle Weight Category")
    plt.tight_layout()
    # Show plot
    plt.show()


# Parameters for plotting, now including weight and frontal area
vehicle_params = {
    "Weight 4.5 tonnes": {"weight": 4500, "area": 2.1},
    "Weight 12 tonnes": {"weight": 12000, "area": 3.5},
    "Weight 24 tonnes": {"weight": 24000, "area": 4.5},
    "Weight 32 tonnes": {"weight": 32000, "area": 5.5},
}

speeds = list(range(20, 121, 10))
grades_degrees = [0]  # Using a single gradient for simplicity in this example

# Execute the plotting function with the specified parameters
plot_speed_vs_fuel_usage_CMEM(vehicle_params, speeds, grades_degrees)

