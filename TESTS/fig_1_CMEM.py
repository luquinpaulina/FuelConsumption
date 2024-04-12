# Import necessary libraries
import matplotlib.pyplot as plt

# Import the CMEM model functions from CMEM_with_degrees.py
from CMEM_with_degrees import *

# Define the plotting function using the imported CMEM model
def plot_speed_vs_fuel_usage_CMEM(weights, speeds, grade_degrees):
    plt.figure(figsize=(10, 6))  # Define figure size for better visibility

    # Loop through each weight category and calculate fuel usage for each speed
    for weight_label, weight in weights.items():
        fuel_usage_list = []
        for speed in speeds:
            # Calculate fuel usage for each scenario using the imported function
            fuel_usage_liters = run_scenario_test(weight, speed, grade_degrees[0])
            fuel_usage_list.append(fuel_usage_liters)

        # Plot the results
        plt.plot(speeds, fuel_usage_list, marker='o', linestyle='-', label=f'Weight: {weight_label}')

    # Customize the plot with title, labels, legend, and grid
    #plt.title('Speed vs. Fuel Usage (CMEM) for Different Loads', fontsize=16) # 1. EXPERIMENT
    #plt.title(' Total fuel consumption for three types of vehicles under different speed levels estimated by CMEM', fontsize=16)
    plt.title('Speed vs Fuel Usage for Different Weight Categories - CMEM', fontsize=16) # 3. EXPERIMENT
    plt.xlabel('Speed (km/h)', fontsize=14)
    plt.ylabel('Fuel Usage (Liters per 100 km)', fontsize=14)
    plt.xticks(speeds)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(title="Vehicle Weight")
    #plt.ylim(0, 45)  # Set y-axis
    #plt.ylim(0, 30)  # Set y-axis # 1. EXPERIMENT
    plt.ylim(0, 70)  # Set y-axis # 3. EXPERIMENT
    plt.tight_layout()
    plt.show()

# Parameters for plotting
#weights_focused = {"4500 kg": 4500, "4500 kg + 15% load": 5175, "4500 kg + 30% load": 5850}  # 1. EXPERIMENT
weights_focused = {"Weight 4.5 tonnes ": 4500, "Weight 12 tonnes ": 12000, "Weight 24 tonnes ": 24000, "Weight 32 tonnes ": 32000}  # Focused analysis on specific loads
#weights_focused = {"0%": 7500, "15%": 8625, "30%": 9750}  # 3. EXPERIMENT
#speeds = list(range(20, 91, 10))  # 1. EXPERIMENT
speeds = list(range(20, 121, 10))  # 2. EXPERIMENT & 3. EXPERIMENT
grades_degrees = [0]  # Using a single gradient for simplicity in this example

# Execute the plotting function with the specified parameters
plot_speed_vs_fuel_usage_CMEM(weights_focused, speeds, grades_degrees)



