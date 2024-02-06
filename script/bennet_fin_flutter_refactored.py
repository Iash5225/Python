from sympy import symbols, lambdify, exp, pi
import numpy as np
import math
import triangle as tr

# Define symbols in one central place
cr, ct, b, h, T, G, t, P, a, AR, lambda_ratio, epsilon, cx, K,m,P0 = symbols(
    'c_r c_t b h T G t P a AR lambda_ratio epsilon cx K m P0')

# cx for trapezoidal fins
cx_expr= ((2*ct*m)+ct**2+(m*cr)+(ct*cr)+cr**2)/(3*(ct+cr))

# Expressions for wing area, aspect ratio, and taper ratio
S_expr = 1/2 * (cr + ct) * b
AR_expr = b**2 / S_expr
lambda_expr = ct / cr

thickness_ratio_expr = t/cr

# Temperature
T_expr_SI = 15-0.0065*h
T_expr_Imperial = 59 - 0.00356 * h


# Pressure
P_expr_SI = 101.325 * ((T_expr_SI + 273.16) / 288.16) ** 5.256
P_expr_Imperial = 14.696 * ((T_expr_Imperial + 459.7) / 518.7) ** 5.256


# speed of sound = a
a_expr_SI = 20.05*(273.16+T)**0.5
a_expr_Imperial = 49.03*(459.7+T)**0.5

# Epsilon
epsilon_expr = (cx_expr/cr)-0.25

# Denominator Constant
DN_expr = (24*epsilon*K*P0)/pi

# First Term
Term1_expr = (DN_expr*AR_expr**3)/((thickness_ratio_expr**3)*(AR_expr+2))
Term2_expr = (lambda_expr+1)/2
Term3_expr_SI = P_expr_SI/101.325
Term3_expr_Imperial = P_expr_Imperial/14.696


# Fin flutter velocity expression
Vf_expr_SI = a_expr_SI * \
    (G / (Term1_expr)*(Term2_expr)*(Term3_expr_SI))**0.5
Vf_expr_Imperial = a_expr_Imperial * \
    (G / (Term1_expr)*(Term2_expr)*(Term3_expr_Imperial))**0.5

# Corrected lambdify functions
temperature_function_SI = lambdify(h, T_expr_SI, modules='numpy')
temperature_function_Imperial = lambdify(h, T_expr_Imperial, modules='numpy')

pressure_function_SI = lambdify(h, P_expr_SI, modules='numpy')
pressure_function_Imperial = lambdify(h, P_expr_Imperial, modules='numpy')

speed_of_sound_function_SI = lambdify(T, a_expr_SI, modules='numpy')
speed_of_sound_function_Imperial = lambdify(
    T, a_expr_Imperial, modules='numpy')

aspect_ratio_function = lambdify((cr, ct, b), AR_expr, modules='numpy')
taper_ratio_function = lambdify((cr, ct), lambda_expr, modules='numpy')

cx_function = lambdify((cr, ct, m), cx_expr, modules='numpy')
epsilon_function = lambdify((cr, ct, m), epsilon_expr, modules='numpy')

flutter_velocity_function_SI = lambdify(
    (G, cr, ct, b, t, m, P, K), Vf_expr_SI, modules=[{"sqrt": np.sqrt}, "numpy", "math"])
flutter_velocity_function_Imperial = lambdify(
    (G, cr, ct, b, t, m, P, K), Vf_expr_Imperial, modules=[{"sqrt": np.sqrt}, "numpy", "math"])


def main():
# Gather input parameters
    print("Enter the following parameters for flutter velocity calculation:")

    # cr_val = float(input("Root chord length (cr): "))
    # ct_val = float(input("Tip chord length (ct): "))
    # b_val = float(input("Span (b): "))
    # h_val = float(input("Height (h): "))
    # t_val = float(input("Thickness (t): "))
    # m_val = float(input("Sweep Length(m): "))
    # G_val = float(input("Shear modulus (G): "))
    # K_val = float(input("Constant K: "))
    # P0_val = float(input("Reference Pressure (P0): "))

    cr_val = 7.5 #inch
    ct_val = 2.5 #inch
    b_val = 3 #inch
    h_val = 4500 # ft
    t_val = 0.1875 #inch
    m_val = 4.285 #inch
    G_val = 600000 # psi
    K_val = 1.4
    P0_val = 14.696

    # Choose unit system
    unit_system = 'imperial'

    # Compute necessary intermediate values
    temperature = (temperature_function_SI if unit_system == "si" else temperature_function_Imperial)(h_val)
    pressure = (pressure_function_SI if unit_system == "si" else pressure_function_Imperial)(temperature)
    speed_of_sound = (speed_of_sound_function_SI if unit_system == "si" else speed_of_sound_function_Imperial)(temperature)
    
    # Compute flutter velocity
    flutter_velocity = (flutter_velocity_function_SI if unit_system == "si" else flutter_velocity_function_Imperial)(
        G_val, cr_val, ct_val, b_val, t_val, m_val, pressure, K_val)

    print(f"Computed Flutter Velocity ({'m/s' if unit_system == 'si' else 'ft/s'}): {flutter_velocity}")

if __name__ == "__main__":
    main()  # Replace with your file path

