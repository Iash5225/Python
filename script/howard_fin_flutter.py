from sympy import symbols, lambdify, sqrt

# Define symbols in one central place
cr, ct, b, h, T, G, t, P, a, AR, lambda_ratio = symbols(
    'c_r c_t b h T G t P a AR lambda_ratio')

# Expressions for wing area, aspect ratio, and taper ratio
S_expr = 1/2 * (cr + ct) * b
AR_expr = b**2 / S_expr
lambda_expr = ct / cr

# Expressions for atmospheric properties
T_expr = 59 - 0.00356 * h
P_expr = 2116/144 * ((T + 459.7) / 518.6) ** 5.256
a_expr = (1.4 * 1716.59 * (T + 460))**0.5

# Fin flutter velocity expression
Vf_expr = a * sqrt(G / (1.337 * AR**3 * P *
                   (lambda_ratio + 1) / (2 * (AR + 2) * (t / cr)**3)))

# Lambdify expressions for numerical calculations
temperature_function = lambdify(h, T_expr, modules='numpy')
pressure_function = lambdify(T, P_expr, modules='numpy')
speed_of_sound_function = lambdify(T, a_expr, modules='numpy')
aspect_ratio_function = lambdify((cr, ct, b), AR_expr, modules='numpy')
taper_ratio_function = lambdify((cr, ct), lambda_expr, modules='numpy')
flutter_velocity_lambdified = lambdify(
        (a, G, AR, P, lambda_ratio, t, cr), Vf_expr, modules='numpy')

# Now, you can call these lambdified functions in your main calculation functions
def calculate_temperature(altitude:float)->float:
    """
    calculate_temperature  Calculate the temperature at a given altitude in Fahrenheit

    Args:
        altitude (float):  The altitude in feet

    Returns:
        float:  The temperature in Fahrenheit
    """    

    return temperature_function(altitude)


def calculate_pressure(altitude:float)->float:
    """
    calculate_pressure  Calculate the pressure at a given altitude in psi

    Args:
        altitude (float):  The altitude in feet

    Returns:
        float:  The pressure in psi
    """    
     
    temperature = calculate_temperature(altitude)
    return pressure_function(temperature)


def calculate_speed_of_sound(altitude:float)->float:
    """
    calculate_speed_of_sound  Calculate the speed of sound at a given altitude in ft/s

    Args:
        altitude (float):  The altitude in feet

    Returns:
        float:  The speed of sound in ft/s
    """     
    
    temperature = calculate_temperature(altitude)
    return speed_of_sound_function(temperature)


def calculate_flutter_velocity(altitude:float, shear_modulus:float, thickness:float, root_chord:float, tip_chord:float, semispan:float)->float:
    """
    calculate_flutter_velocity  Calculate the flutter velocity at a given altitude in ft/s

    Args:
        altitude (float):  The altitude in feet
        shear_modulus (float):  The shear modulus in psi
        thickness (float):  The thickness in inches
        root_chord (float):  The root chord in inches
        tip_chord (float):  The tip chord in inches
        semispan (float):  The semispan in inches

    Returns:
        float:  The flutter velocity in ft/s
    """    
    aspect_ratio = aspect_ratio_function(root_chord, tip_chord, semispan)
    taper_ratio = taper_ratio_function(root_chord, tip_chord)
    pressure = calculate_pressure(altitude)
    speed_of_sound = calculate_speed_of_sound(altitude)

    flutter_velocity = flutter_velocity_lambdified(
        speed_of_sound, shear_modulus, aspect_ratio, pressure, taper_ratio, thickness, root_chord)

    return flutter_velocity
