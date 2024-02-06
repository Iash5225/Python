from sympy import symbols, lambdify, sqrt, exp, pi, cos
import numpy as np
import math
import triangle as tr

from script.sahr_fin_flutter import P0

# Define symbols in one central place
cr, ct, b, h, T, G, t, P, a, AR, lambda_ratio, epsilon, cx, K,m = symbols(
    'c_r c_t b h T G t P a AR lambda_ratio epsilon cx K m')

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
a_expr_SI = 20.05*sqrt(273.16+T)
a_expr_Imperial = 49.03*sqrt(459.7+T)

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
Vf_expr_SI = a_expr_SI * sqrt(G / (Term1_expr)*(Term2_expr)*(Term3_expr_SI))
Vf_expr_Imperial = a_expr_Imperial * \
    sqrt(G / (Term1_expr)*(Term2_expr)*(Term3_expr_Imperial))

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
    (G, cr, ct, b, t, m, P, K), Vf_expr_SI, modules='numpy')
flutter_velocity_function_Imperial = lambdify(
    (G, cr, ct, b, t, m, P, K), Vf_expr_Imperial, modules='numpy')

if __name__ == "__main__":
    main()  # Replace with your file path

