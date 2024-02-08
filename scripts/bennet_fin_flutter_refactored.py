from sympy import symbols, lambdify, exp, pi, N
import numpy as np
import math
import triangle as tr

# Define symbols in one central place
cr, ct, b, h, T, G, t, P, a, AR, lambda_ratio, epsilon, cx, K, m, P0, T1, T2, T3 = symbols(
    'c_r c_t b h T G t P a AR lambda_ratio epsilon cx K m P0 T1 T2 T3')

# cx for trapezoidal fins
cx_expr = ((2*ct*m)+ct**2+(m*cr)+(ct*cr)+cr**2)/(3*(ct+cr))

# Expressions for wing area, aspect ratio, and taper ratio
S_expr = 1/2 * (cr + ct) * b
AR_expr = b**2 / S_expr
lambda_expr = ct / cr

thickness_ratio_expr = t/cr

# Temperature
T_expr_SI = 15-0.0065*h
T_expr_Imperial = 59 - 0.00356 * h


# Pressure
P_expr_SI = 101.325 * ((T + 273.16) / 288.16) ** 5.256
P_expr_Imperial = 14.696 * ((T + 459.7) / 518.7) ** 5.256


# speed of sound = a
a_expr_SI = 20.05*(273.16+T)**0.5
a_expr_Imperial = 49.03*(459.7+T)**0.5

# Epsilon
epsilon_expr = (cx_expr/cr)-0.25

# Denominator Constant
DN_expr = (24*epsilon*K*P0)/np.pi

# First Term
Term1_expr = (DN_expr*AR_expr**3)/((thickness_ratio_expr**3)*(AR_expr+2))
Term2_expr = (lambda_expr+1)/2
Term3_expr_SI = P_expr_SI/101.325
Term3_expr_Imperial = P_expr_Imperial/14.696


# Fin flutter velocity expression
# Fin flutter velocity expression
# Vf_expr_SI = a_expr_SI * (G / (Term1_expr * Term2_expr * Term3_expr_SI))**0.5
# Vf_expr_Imperial = a_expr_Imperial * \
#     (G / (Term1_expr * Term2_expr * Term3_expr_Imperial))**0.5

Vf_expr = a*(G/(T1 * T2 * T3))**0.5

# Corrected lambdify functions
temperature_function_SI = lambdify(h, T_expr_SI, modules='numpy')
temperature_function_Imperial = lambdify(h, T_expr_Imperial, modules='numpy')

pressure_function_SI = lambdify(T, P_expr_SI, modules='numpy')
pressure_function_Imperial = lambdify(T, P_expr_Imperial, modules='numpy')

speed_of_sound_function_SI = lambdify(T, a_expr_SI, modules='numpy')
speed_of_sound_function_Imperial = lambdify(
    T, a_expr_Imperial, modules='numpy')

aspect_ratio_function = lambdify((cr, ct, b), AR_expr, modules='numpy')
taper_ratio_function = lambdify((cr, ct), lambda_expr, modules='numpy')

cx_function = lambdify((cr, ct, m), cx_expr, modules='numpy')
epsilon_function = lambdify((cr, ct, m), epsilon_expr, modules='numpy')

# flutter_velocity_function_SI = lambdify(
#     (G, cr, ct, b, t, m, P, K), Vf_expr_SI, modules='numpy')
flutter_velocity_function_Imperial = lambdify(
    (G, cr, ct, b, t, m, P, K), Vf_expr, modules='numpy')

# Define a function to substitute and evaluate expressions


def evaluate_flutter_velocity(G_val, cr_val, ct_val, b_val, t_val, m_val, P_val, K_val, P0_val, a_val, T_val):
    # First, calculate any dependent expressions
    # Assuming cx_function is correctly defined
    cx_val = cx_function(cr_val, ct_val, m_val)
    # Assuming epsilon_function is correctly defined
    epsilon_val = epsilon_function(cr_val, ct_val, m_val)

    # Now substitute all terms in Term1
    term1 = Term1_expr.subs({
        G: G_val,
        cr: cr_val,
        ct: ct_val,
        b: b_val,
        t: t_val,
        m: m_val,
        P: P_val,
        K: K_val,
        P0: P0_val,
        epsilon: epsilon_val
    })
    term2 = Term2_expr.subs({cr: cr_val, ct: ct_val})
    # term3 = Term3_expr_Imperial.subs({T: T_val, P: P_val})
    
    term3 = Term3_expr_SI.subs({T: T_val, P: P_val})
#     print(f"term1={term1}")
#     print(f"term2={term2}")
#     print(f"term3={term3}")

    vf_expr_evaluated = Vf_expr.subs(
        {a: a_val, G: G_val, T1: term1, T2: term2, T3: term3})
    # Numerical evaluation
    vf_numerical = N(vf_expr_evaluated)

    return vf_numerical


def compute_and_print_flutter_velocity(unit_system, cr_val, ct_val, b_val, h_val, t_val, m_val, G_val, K_val, P0_val):
    # Choose the correct functions based on the unit system
    temperature_function = temperature_function_SI if unit_system == "si" else temperature_function_Imperial
    pressure_function = pressure_function_SI if unit_system == "si" else pressure_function_Imperial
    speed_of_sound_function = speed_of_sound_function_SI if unit_system == "si" else speed_of_sound_function_Imperial

    # Compute temperature, pressure, and speed of sound
    temperature = temperature_function(h_val)
    pressure = pressure_function(temperature)
    speed_of_sound = speed_of_sound_function(temperature)

#     # Print intermediate values for verification
#     print(
#         f"Temperature = {temperature} {'Celsius' if unit_system == 'si' else 'Fahrenheit'}")
#     print(f"Pressure = {pressure} {'kPa' if unit_system == 'si' else 'psi'}")
#     print(
#         f"Speed of Sound = {speed_of_sound} {'m/s' if unit_system == 'si' else 'ft/s'}")

    # Evaluate and compute flutter velocity
    flutter_velocity = evaluate_flutter_velocity(
        G_val, cr_val, ct_val, b_val, t_val, m_val, pressure, K_val, P0_val, speed_of_sound, temperature)

#     # Print computed flutter velocity
#     print(
#         f"Computed Flutter Velocity: {flutter_velocity} {'m/s' if unit_system == 'si' else 'ft/s'}")
    return flutter_velocity


# Example usage
# if __name__ == "__main__":
#     unit_system = 'si'  # or 'Imperial'
#     cr_val = 30.0  # Root chord length
#     ct_val = 10.0  # Tip chord length
#     b_val = 14.0  # Wingspan
#     h_val = 0 + 3048.0  # Altitude in meters or feet
#     t_val = 0.4  # Thickness
#     m_val = 9.0  # Sweep length in cm or inches
#     G_val = 5000000.0  # Shear modulus in kPa or psi
#     K_val = 1.4  # Specific heat ratio
#     P0_val = 101.325  # Standard pressure in kPa or psi

#     # Call the encapsulated method
#     compute_and_print_flutter_velocity(
#         unit_system, cr_val, ct_val, b_val, h_val, t_val, m_val, G_val, K_val, P0_val)
