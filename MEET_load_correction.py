import math

# DATA TABLES MEET

# Dictionary format: {Weight class: {'K': value, 'a': value, 'b': value, 'c': value, 'd': value, 'e': value, 'f': value}}
emission_parameters = {
    "3.5_to_7.5": {'K': 110, 'a': 0, 'b': 0, 'c': 0.000375, 'd': 8702, 'e': 0, 'f': 0},
    "7.5_to_16": {'K': 871, 'a': -16.0, 'b': 0.143, 'c': 0, 'd': 0, 'e': 32031, 'f': 0},
    "16_to_32": {'K': 765, 'a': -7.04, 'b': 0, 'c': 0.000632, 'd': 8334, 'e': 0, 'f': 0},
    "above_32": {'K': 1576, 'a': -17.6, 'b': 0, 'c': 0.00117, 'd': 0, 'e': 36067, 'f': 0}
}

load_correction_factors = {
    "Weight_<=7.5": {'k': 1.27, 'n': 0.0614, 'p': 0, 'q': -0.00110, 'r': -0.00235, 's': 0, 't': 0, 'u': -1.33},
    "Weight_7.5_to_16": {'k': 1.26, 'n': 0.0790, 'p': 0, 'q': -0.00109, 'r': 0, 's': 0, 't': -2.03E-7, 'u': -1.14},
    "Weight_16_to_32": {'k': 1.27, 'n': 0.0882, 'p': 0, 'q': -0.00101, 'r': 0, 's': 0, 't': 0, 'u': -0.483},
    "Weight_>32": {'k': 1.43, 'n': 0.121, 'p': 0, 'q': -0.00125, 'r': 0, 's': 0, 't': 0, 'u': -0.916}
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

def get_load_correction_factors(weight):
    """
    Select the appropriate load correction factors based on vehicle weight.
    """
    if weight <= 7.5:
        return load_correction_factors["Weight_<=7.5"]
    elif 7.5 < weight <= 16:
        return load_correction_factors["Weight_7.5_to_16"]
    elif 16 < weight <= 32:
        return load_correction_factors["Weight_16_to_32"]
    else:
        return load_correction_factors["Weight_>32"]


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



# SECOND FORMULA - LOAD CORRECTION FACTOR
def calculate_load_correction_factor(weight, speed, gradient_percentage):
    """
    Calculate the load correction factor using the MEET model formula. (2.15)
    """
    # Get the load correction factors for the given weight class
    params = get_load_correction_factors(weight)

    # Calculate load_correction_factor
    load_correction_factor = (params['k'] +
                              params['n'] * gradient_percentage +
                              params['p'] * gradient_percentage**2 +
                              params['q'] * gradient_percentage**3 +
                              params['r'] / speed +
                              params['s'] / speed**2 +
                              params['t'] / speed**3 +
                              params['u'] / speed)

    return load_correction_factor


def calculate_total_CO2_emissions(emissions_rate, load_correction_factor, distance):
    """
    Calculate the total CO2 emissions using the MEET model. (2.16)
    """
    # Calculate the total CO2 emissions
    total_CO2_emissions = emissions_rate * load_correction_factor * distance

    return total_CO2_emissions


'''def convert_CO2_to_fuel_liters(CO2_emissions_grams, CO2_emissions_factor=3152): #This number affects a lot, we use this for our results Demir
    """
    Convert CO2 emissions in grams to fuel consumption in liters.
    CO2_emissions_factor is the grams of CO2 produced per liter of fuel.
    """
    return CO2_emissions_grams / CO2_emissions_factor'''

def convert_CO2_to_fuel_liters(CO2_emissions_grams, CO2_emissions_factor=3197.2): #This number affects a lot, we use this for our results Demir
    """
    Convert CO2 emissions in grams to fuel consumption in liters.
    CO2_emissions_factor is the grams of CO2 produced per liter of fuel.
    """
    return CO2_emissions_grams / CO2_emissions_factor



