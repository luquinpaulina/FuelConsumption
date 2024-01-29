import matplotlib.pyplot as plt

# DATA TABLES MEET

# Dictionary format: {Weight class: {'K': value, 'a': value, 'b': value, 'c': value, 'd': value, 'e': value, 'f': value}}
emission_parameters = {
    "3.5_to_7.5": {'K': 110, 'a': 0, 'b': 0, 'c': 0.000375, 'd': 8702, 'e': 0, 'f': 0},
    "7.5_to_16": {'K': 871, 'a': -16.0, 'b': 0.143, 'c': 0, 'd': 0, 'e': 32031, 'f': 0},
    "16_to_32": {'K': 765, 'a': -7.04, 'b': 0, 'c': 0.000632, 'd': 8334, 'e': 0, 'f': 0},
    "above_32": {'K': 1576, 'a': -17.6, 'b': 0, 'c': 0.00117, 'd': 0, 'e': 36067, 'f': 0}
}

# FIRST METHOD GET EMISSION PARAMETER
def get_emission_parameters(weight):
    """
    Select the appropriate emission parameters based on vehicle weight.
    """
    if weight <= 7.5:
        return emission_parameters["3.5_to_7.5"]
    elif 7.5 < weight <= 16:
        return emission_parameters["7.5_to_16"]
    elif 16 < weight <= 32:
        return emission_parameters["16_to_32"]
    else:
        return emission_parameters["above_32"]

# FIRST FORMULA FUEL CONSUMPTION
def calculate_emissions(weight, speed):
    """
    Calculate the rate of emissions using the MEET model formula. (2.13)
    """
    # Get the emission parameters for the given weight class
    params = get_emission_parameters(weight)

    # Calculate the rate of emissions (g/km)
    emissions_rate = (params['K'] +
                      params['a'] * speed +
                      params['b'] * speed**2 +
                      params['c'] * speed**3 +
                      params['d'] / speed +
                      params['e'] / speed**2 +
                      params['f'] / speed**3)

    return emissions_rate

def calculate_total_CO2_emissions(emissions_rate, distance):
    """
    Calculate the total CO2 emissions using the MEET model. (2.16)
    """
    # Calculate the total CO2 emissions
    total_CO2_emissions = emissions_rate * distance

    return total_CO2_emissions

def convert_CO2_to_fuel_liters(CO2_emissions_grams, CO2_emissions_factor=2680):
    """
    Convert CO2 emissions in grams to fuel consumption in liters.
    CO2_emissions_factor is the grams of CO2 produced per liter of fuel.
    """
    return CO2_emissions_grams / CO2_emissions_factor


## EXPERIEMENTS
## DOING FIGURE 2 of Jabali, Van Woensel, and de Kok (2012) - (TABU SEARCH) - Analysis of Travel Times and CO2 Emissions in Time-Dependent Vehicle Routing
def calculate_emissions_for_speeds(weight, min_speed, max_speed, step, distance):
    """
    Calculate total CO2 emissions in kg/km for various speeds within a specified range for a given weight.
    """
    results = {}
    for speed in range(min_speed, max_speed + 1, step):
        emissions_rate = calculate_emissions(weight, speed)
        total_CO2 = calculate_total_CO2_emissions(emissions_rate, distance)
        total_CO2_kg_per_km = (total_CO2 / 1000) / distance  # Convert to kg/km
        results[speed] = total_CO2_kg_per_km

    return results

# Example usage
weight = 33  # Numerical weight value for "above_32" class
min_speed = 30  # Minimum speed in km/h
max_speed = 118  # Maximum speed in km/h
step = 4  # Increment step in km/h
distance = 100  # Distance in km

emissions_results = calculate_emissions_for_speeds(weight, min_speed, max_speed, step, distance)
for speed, total_CO2_kg_per_km in emissions_results.items():
    print(f"Speed: {speed} km/h, Total CO2 Emissions: {total_CO2_kg_per_km} kg/km")


# PLOT FIG 2
def plot_emissions(speeds, emissions):
    plt.figure(figsize=(10, 6))
    plt.plot(speeds, emissions, marker='o')

    # Set the title and labels
    plt.title('CO2 Emissions vs Speed')
    plt.xlabel('Speed (km/h)')
    plt.ylabel('CO2 Emissions (kg/km)')

    # Set x and y ticks
    plt.xticks(range(30, 119, 4))  # X-axis ticks from 30 to 118, in steps of 4
    plt.yticks([i / 10.0 for i in range(6, 17, 2)])  # Y-axis ticks from 0.6 to 1.6, in steps of 0.2

    # Enable grid
    plt.grid(True)

    # Show the plot
    plt.show()

# emissions_results is a dictionary with speeds as keys and CO2 emissions as values
speeds = list(emissions_results.keys())
emissions = list(emissions_results.values())

plot_emissions(speeds, emissions)



