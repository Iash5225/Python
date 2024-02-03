from sympy import symbols, lambdify, sqrt, exp
import numpy as np

# Define symbols in one central place
cr, ct, b, h, H, T, G, t, P0, Cs0, B, lambda_ratio, Vf = symbols(
    'c_r c_t b h H T G t P_0 C_s0 B lambda_ratio Vf')

# Expressions for wing area, aspect ratio, and taper ratio
S_expr = 1/2 * (cr + ct) * b
B_expr = b**2 / S_expr
lambda_expr = ct / cr
T_expr = t/cr

# Fin flutter velocity expression
Vf_expr = 1.223 * Cs0 * exp(0.4*h/H)*sqrt(G/P0) * \
    sqrt((2+B)/(1+lambda_ratio))*(T/B)**(3/2)

t_expr = (cr*B)*(Vf/(1.223 * Cs0 * exp(0.4*h/H)*sqrt(G/P0) *
                sqrt((2+B)/(1+lambda_ratio))))**(2/3)

# Lambdify expressions for numerical calculations
normalised_thickness_function = lambdify((t, cr), T_expr, modules='numpy')
aspect_ratio_function = lambdify((cr, ct, b), B_expr, modules='numpy')
taper_ratio_function = lambdify((cr, ct), lambda_expr, modules='numpy')
flutter_velocity_lambdified = lambdify(
    (Cs0, h, H, G, P0, B, lambda_ratio, T), Vf_expr, modules='numpy')
thickness_function = lambdify(
    (cr, Vf, Cs0, h, H, G, P0, B, lambda_ratio), t_expr, modules='numpy')

# Now, you can call these lambdified functions in your main calculation functions
def calculate_normalised_thickness(thickness:float, root_chord:float)->float:
    """
    calculate_normalised_thickness  Calculate the normalised thickness of a fin

    Args:
        thickness (float):  The thickness of the fin in inches
        root_chord (float):  The root chord of the fin in inches

    Returns:
        float:  The normalised thickness of the fin
    """    
    
    return normalised_thickness_function(thickness, root_chord)


def calculate_flutter_velocity(sea_level_speed_of_sound:float, altitude:float, atmospheric_scale_height:float, shear_modulus:float, sea_level_pressure:float, thickness:float, root_chord:float, tip_chord:float, semispan:float)->float:
    """
    calculate_flutter_velocity  Calculate the flutter velocity of a fin

    Args:
        sea_level_speed_of_sound (float):  The speed of sound at sea level in m/s
        altitude (float):  The altitude in m 
        atmospheric_scale_height (float):  The atmospheric scale height in m
        shear_modulus (float):  The shear modulus of the fin material in Pa
        sea_level_pressure (float):  The sea level pressure in Pa
        thickness (float):  The thickness of the fin in m
        root_chord (float):  The root chord of the fin in m
        tip_chord (float):  The tip chord of the fin in m
        semispan (float):  The semispan of the fin in m

    Returns:
        float:  The flutter velocity of the fin in m/s
    """    
    aspect_ratio = aspect_ratio_function(root_chord, tip_chord, semispan)
    taper_ratio = taper_ratio_function(root_chord, tip_chord)
    normalised_thickness = calculate_normalised_thickness(
        thickness=thickness, root_chord=root_chord)

    flutter_velocity = flutter_velocity_lambdified(
        sea_level_speed_of_sound, altitude, atmospheric_scale_height, shear_modulus, sea_level_pressure, aspect_ratio, taper_ratio, normalised_thickness)

    return flutter_velocity


def list_of_flutter_velocities(minimum_thickness: float, maximum_thickness: float, increments: float, sea_level_speed_of_sound: float, altitude: float, atmospheric_scale_height: float, shear_modulus: float, sea_level_pressure: float, root_chord: float, tip_chord: float, semispan: float) -> np.ndarray:
    """
    list_of_flutter_velocities  Generate a list of flutter velocities for a range of fin thicknesses

    Args:
        minimum_thickness (float): Minimum thickness of the fin in m
        maximum_thickness (float): Maximum thickness of the fin in m
        increments (float): Increment value for thickness in m
        sea_level_speed_of_sound (float): Speed of sound at sea level in m/s
        altitude (float): Altitude in m
        atmospheric_scale_height (float): Atmospheric scale height in m
        shear_modulus (float): Shear modulus of the fin material in Pa
        sea_level_pressure (float): Sea level pressure in Pa
        root_chord (float): Root chord of the fin in m
        tip_chord (float): Tip chord of the fin in m
        semispan (float): Semispan of the fin in m

    Returns:
        np.ndarray: Array of flutter velocities for each thickness in m/s
    """
    # Create array of thickness values
    thicknesses = np.arange(
        minimum_thickness, maximum_thickness + increments, increments)

    # Calculate flutter velocity for each thickness
    flutter_velocities = np.array([calculate_flutter_velocity(sea_level_speed_of_sound, altitude, atmospheric_scale_height,
                                  shear_modulus, sea_level_pressure, thickness, root_chord, tip_chord, semispan) for thickness in thicknesses])

    return flutter_velocities
