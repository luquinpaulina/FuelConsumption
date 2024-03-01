def calculate_gradient_correction_factor(speed):

    '''A6 = 0
    A5 = -3.01E-09
    A4 = 5.73E-07
    A3 = -4.13E-05
    A2 = 1.13E-03
    A1 = 8.13E-03
    A0 = 9.14E-01'''

    A6 = 0
    A5 = -1.39E-10
    A4 = 5.03E-08
    A3 = -4.18E-06
    A2 = 1.95E-05
    A1 = 3.68E-03
    A0 = 9.69E-01

    # Calculate the gradient correction factor (GC) based on the formula provided
    GC = ( A6 * speed ** 6 +
           A5 * speed ** 5 +
           A4 * speed ** 4 +
           A3 * speed ** 3 +
           A2 * speed ** 2 +
           A1 * speed +
           A0
          )

    return GC

# Example usage
speed = 70
GC = calculate_gradient_correction_factor(speed)
print(GC)
