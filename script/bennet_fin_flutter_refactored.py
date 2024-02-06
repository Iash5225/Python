from sympy import symbols, lambdify, sqrt, exp, pi, cos
import numpy as np
import math

# Define symbols
MaxV, AMaxV, LSA, TLS, DEF, Thickness, TC, RC, Height, GE, T2T, fin_area, fin_Cx = symbols(
    'MaxV AMaxV LSA TLS DEF Thickness TC RC Height GE T2T fin_area fin_Cx')
airP, Temp, Spd_of_Sound, Term1, Term2, Term3, Vf = symbols(
    'airP Temp Spd_of_Sound Term1 Term2 Term3 Vf')

# Expressions for Fin Area and Center of Pressure (Cx)
# These would be computed from the given fin vertex data
# For now, let's assume they are inputs

# Expressions for Fin Flutter Velocity
Fin_Eps_expr = (fin_Cx / RC) - 0.25
ThicknessRatio_expr = Thickness / RC
Lambda_expr = TC / RC
AspectRatio_expr = (Height**2) / fin_area
DN_expr = (24 * Fin_Eps_expr * 1.4 * airP) / pi
Term1_expr = (DN_expr * AspectRatio_expr**3) / \
    (ThicknessRatio_expr**3 * (AspectRatio_expr + 2))
Term2_expr = (Lambda_expr + 1)/2
Term3_expr = airP / airP  # Assuming sea-level pressure for simplicity
Vf_expr = Spd_of_Sound * sqrt(GE/(Term1_expr * Term2_expr * Term3_expr))

# Lambdify expressions for numerical calculations
fin_area_and_cx_function = lambdify(
    (fin_area, fin_Cx), (fin_area, fin_Cx), modules='numpy')
flutter_velocity_function = lambdify(
    (airP, Temp, Spd_of_Sound, GE, RC, Height, TC, Thickness, fin_Cx), Vf_expr, modules='numpy')
