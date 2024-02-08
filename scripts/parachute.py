from sympy import symbols, lambdify, sqrt, exp, pi
import numpy as np

# Define symbols
Fd, rho, Cd, A, v, Fg, m, g, D = symbols('F_d rho C_d A v F_g m g D')

# Expression for parachute diameter
chute_diameter_expr = sqrt((8*m*g)/(pi*rho*Cd*v**2))
velocity_expr = sqrt((8 * m * g) / (pi * rho * Cd * D**2))
drag_coefficient_expr = (8 * m * g) / (pi * rho * D**2 * v**2)

# Lambdify expressions for numerical calculations
velocity_function = lambdify(
    (m, g, rho, Cd, D), velocity_expr, modules='numpy')
drag_coefficient_function = lambdify(
    (m, g, rho, D, v), drag_coefficient_expr, modules='numpy')

# Lambdify the expression for numerical calculations
chute_diameter_function = lambdify(
    (m, g, rho, Cd, v), chute_diameter_expr, modules='numpy')


def calc_chute_diameter(mass: float, gravity: float, air_density: float, drag_coefficient: float, velocity: float) -> float:
    # Call the lambdified function with the parameters
    return chute_diameter_function(mass, gravity, air_density, drag_coefficient, velocity)


def calc_velocity(mass: float, gravity: float, air_density: float, drag_coefficient: float, diameter: float) -> float:
    return velocity_function(mass, gravity, air_density, drag_coefficient, diameter)


def calc_drag_coefficient(mass: float, gravity: float, air_density: float, diameter: float, velocity: float) -> float:
    return drag_coefficient_function(mass, gravity, air_density, diameter, velocity)


def list_of_chute_diameters(minimum_velocity: float, maximum_velocity: float, increments: float, mass: float, gravity: float, air_density: float, drag_coefficient: float) -> np.ndarray:
    """
    list_of_chute_diameters  Generate a list of parachute diameters for a range of descent velocities

    Args:
        minimum_velocity (float): Minimum descent velocity in m/s
        maximum_velocity (float): Maximum descent velocity in m/s
        increments (float): Increment value for velocity in m/s
        mass (float): Mass of the object in kg
        gravity (float): Acceleration due to gravity in m/s^2
        air_density (float): Air density in kg/m^3
        drag_coefficient (float): Drag coefficient (dimensionless)

    Returns:
        np.ndarray: Array of parachute diameters for each descent velocity in m
    """
    # Create array of velocity values
    velocities = np.arange(
        minimum_velocity, maximum_velocity + increments, increments)

    # Calculate chute diameter for each velocity
    chute_diameters = np.array([chute_diameter_function(
        mass, gravity, air_density, drag_coefficient, velocity) for velocity in velocities])

    return chute_diameters


def list_of_velocities(minimum_diameter: float, maximum_diameter: float, increments: float, mass: float, gravity: float, air_density: float, drag_coefficient: float) -> np.ndarray:
    """
    list_of_velocities  Generate a list of descent velocities for a range of parachute diameters

    Args:
        minimum_diameter (float): Minimum parachute diameter in m
        maximum_diameter (float): Maximum parachute diameter in m
        increments (float): Increment value for diameter in m
        mass (float): Mass of the object in kg
        gravity (float): Acceleration due to gravity in m/s^2
        air_density (float): Air density in kg/m^3
        drag_coefficient (float): Drag coefficient (dimensionless)

    Returns:
        np.ndarray: Array of descent velocities for each parachute diameter in m/s
    """
    # Create array of diameter values
    diameters = np.arange(
        minimum_diameter, maximum_diameter + increments, increments)

    # Calculate velocity for each diameter
    velocities = np.array([calc_velocity(
        mass, gravity, air_density, drag_coefficient, diameter) for diameter in diameters])

    return velocities