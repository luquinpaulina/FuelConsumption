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

road_gradient_parameters = {
    "Weight_<=7.5": {
        "[0,4]": {'A6': 0, 'A5': -3.01E-09, 'A4': 5.73E-07, 'A3': -4.13E-05, 'A2': 1.13E-03, 'A1': 8.13E-03, 'A0': 9.14E-01},
        "[-4,0]": {'A6': 0, 'A5': -1.39E-10, 'A4': 5.03E-08, 'A3': -4.18E-06, 'A2': 1.95E-05, 'A1': 3.68E-03, 'A0': 9.69E-01}
    },
    "Weight_7.5_to_16": {
        "[0,4]": {'A6': 0, 'A5': -9.78E-10, 'A4': -2.01E-09, 'A3': 1.91E-05, 'A2': -1.63E-03, 'A1': 5.91E-02, 'A0': 7.70E-01},
        "[-4,0]": {'A6': 0, 'A5': -6.04E-11, 'A4': -2.36E-08, 'A3': 7.76E-06, 'A2': -6.83E-04, 'A1': 1.79E-02, 'A0': 6.12E-01}
    },
    "Weight_16_to_32": {
        "[0,4]": {'A6': 0, 'A5': -5.25E-09, 'A4': 9.93E-07, 'A3': -6.74E-05, 'A2': 2.06E-03, 'A1': -1.96E-02, 'A0': 1.45E+00},
        "[-4,0]": {'A6': 0, 'A5': -8.24E-11, 'A4': 2.91E-08, 'A3': -2.58E-06, 'A2': 5.76E-05, 'A1': -4.74E-03, 'A0': 8.55E-01}
    },
    "Weight_>32": {
        "[0,4]": {'A6': 0, 'A5': -2.04E-09, 'A4': 4.35E-07, 'A3': -3.69E-05, 'A2': 1.69E-03, 'A1': -3.16E-02, 'A0': 1.77E+00},
        "[-4,0]": {'A6': 0, 'A5': -1.10E-09, 'A4': 2.69E-07, 'A3': -2.38E-05, 'A2': 9.51E-04, 'A1': -2.24E-02, 'A0': 9.16E-01}
    }
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


def get_road_gradient_parameters(weight, slope_range):
    """
    Select the appropriate road gradient parameters based on vehicle weight and slope range.

    :param weight: Vehicle weight in tons
    :param slope_range: Slope range as a string, either "[0,4]" for uphill or "[-4,0]" for downhill gradients
    :return: A dictionary of road gradient parameters for the specified weight class and slope range
    """
    # Ensure the slope_range is one of the expected values
    if slope_range not in ["[0,4]", "[-4,0]"]:
        raise ValueError("Invalid slope_range. Expected '[0,4]' or '[-4,0]'.")

    # Select the appropriate dictionary based on weight class
    if weight <= 7.5:
        return road_gradient_parameters["Weight_<=7.5"][slope_range]
    elif 7.5 < weight <= 16:
        return road_gradient_parameters["Weight_7.5_to_16"][slope_range]
    elif 16 < weight <= 32:
        return road_gradient_parameters["Weight_16_to_32"][slope_range]
    else:  # weight > 32
        return road_gradient_parameters["Weight_>32"][slope_range]


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


def calculate_gradient_correction_factor(weight, speed, slope_range):
    """
    Calculate the gradient correction factor for emissions or fuel consumption.
    """
    # Retrieve the gradient correction coefficients for the given weight class
    gradient_params = get_road_gradient_parameters(weight, slope_range)

    # Calculate the gradient correction factor (GC) based on the formula provided
    GC = (gradient_params['A6'] * speed ** 6 +
          gradient_params['A5'] * speed ** 5 +
          gradient_params['A4'] * speed ** 4 +
          gradient_params['A3'] * speed ** 3 +
          gradient_params['A2'] * speed ** 2 +
          gradient_params['A1'] * speed +
          gradient_params['A0'])

    return GC


def calculate_total_CO2_emissions(emissions_rate, load_correction_factor, GC, distance):
    """
    Calculate the total CO2 emissions using the MEET model. (2.16)
    """
    # Calculate the total CO2 emissions
    total_CO2_emissions = emissions_rate * load_correction_factor * GC * distance

    return total_CO2_emissions

def convert_CO2_to_fuel_liters(CO2_emissions_grams, CO2_emissions_factor=3197.2): #This number affects a lot, we use this for our results Demir
    """
    Convert CO2 emissions in grams to fuel consumption in liters.
    CO2_emissions_factor is the grams of CO2 produced per liter of fuel.
    """
    return CO2_emissions_grams / CO2_emissions_factor

'''def convert_CO2_to_fuel_liters(CO2_emissions_grams, CO2_emissions_factor=3029.568006077124): #This number affects a lot, we use this for our results Demir
    """
    Convert CO2 emissions in grams to fuel consumption in liters.
    CO2_emissions_factor is the grams of CO2 produced per liter of fuel.
    """
    return CO2_emissions_grams / CO2_emissions_factor'''

