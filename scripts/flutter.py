from sympy import symbols, lambdify, N, sqrt
import numpy as np

# Define symbols
cr, ct, b, h, T, G, t, P, m, K, P0,epsilon,DN,AR, tr,a,T1,T2,T3 = symbols('c_r c_t b h T G t P m K P0 epsilon DN AR tr a T1 T2 T3')

# Expressions
S_expr = 1/2 * (cr + ct) * b
AR_expr = b**2 / S_expr
lambda_expr = ct / cr
thickness_ratio_expr = t/cr
cx_expr = ((2*ct*m)+ct**2+(m*cr)+(ct*cr)+cr**2)/(3*(ct+cr))
epsilon_expr = (cx_expr/cr)-0.25

# Imperial Expressions
T_expr_Imperial = 59 - 0.00356 * h
P_expr_Imperial = 14.696 * ((T + 459.7) / 518.7) ** 5.256
a_expr_Imperial = 49.03*(459.7+T)**0.5
Term3_expr_Imperial = P_expr_Imperial/14.696

# SI Expressions
T_expr_SI = 15 - 0.0065 * h
P_expr_SI = 101.325 * ((T + 273.15) / 288.15) ** 5.256
a_expr_SI = 20.05 * (T + 273.15)**0.5
Term3_expr_SI = P_expr_SI / 101.325

# Flutter Velocity Expressions
DN_expr = (24*epsilon*K*P0)/np.pi
Term1_expr = (DN*AR**3)/((tr**3)*(AR+2))
Term2_expr = (lambda_expr+1)/2
Vf_expr_Imperial = a_expr_Imperial * \
    (G / (Term1_expr * Term2_expr * Term3_expr_Imperial))**0.5
    
# Vf_expr_SI = a_expr_SI * (G / (Term1_expr * Term2_expr * Term3_expr_SI))**0.5

# Vf_expr_SI = a * sqrt((G / (T1 * T2 * T3)))
Vf_expr_SI = a*(G/(T1 * T2 * T3))**0.5
# Lambdify functions
temperature_function = {
    "SI": lambdify(h, T_expr_SI, modules='numpy'),
    "Imperial": lambdify(h, T_expr_Imperial, modules='numpy')
}
pressure_function = {
    "SI": lambdify(T, P_expr_SI, modules='numpy'),
    "Imperial": lambdify(T, P_expr_Imperial, modules='numpy')
}
speed_of_sound_function = {
    "SI": lambdify(T, a_expr_SI, modules='numpy'),
    "Imperial": lambdify(T, a_expr_Imperial, modules='numpy')
}
# flutter_velocity_function = {
#     "SI": lambdify((G, cr, ct, b, t, m, P, K, P0, T), Vf_expr_SI, modules='numpy'),
#     "Imperial": lambdify((G, cr, ct, b, t, m, P, K, P0, T), Vf_expr_Imperial, modules='numpy')
# }
flutter_velocity_function = {
    "SI": lambdify((a, G, T1, T2, T3), Vf_expr_SI, modules='numpy'),
    # "Imperial": lambdify((G, cr, ct, b, t, m, P, K, P0, T), Vf_expr_Imperial, modules='numpy')
}

# Main function


def main():
    # Input parameters
    unit_system = "SI"
    cr_val = 30.0  # cm based on unit system
    ct_val = 10.0  # cm
    b_val = 14.0  # cm
    h_val = 0 + 3048.0  # meters
    t_val = 0.4  # cm
    m_val = 9.0  # inch or cm Sweep Length
    # G_val = 4136854  # psi or kPa
    G_val = 5000000.0  # notebook value
    K_val = 1.4  # constant
    P0_val = 14.696 if unit_system == "Imperial" else 101.325  # psi or kPa

    # Compute intermediate values
    temperature = temperature_function[unit_system](h_val)
    pressure = pressure_function[unit_system](temperature)
    speed_of_sound = speed_of_sound_function[unit_system](temperature)

    # Calculate cx, epsilon, DN, AR, thickness ratio, and Term1, Term2, Term3
    cx_val = cx_expr.subs({cr: cr_val, ct: ct_val, m: m_val}).evalf()
    epsilon_val = epsilon_expr.subs({cx_expr: cx_val, cr: cr_val}).evalf()
    DN_val = DN_expr.subs({epsilon: epsilon_val, K: K_val, P0: P0_val}).evalf()
    AR_val = AR_expr.subs({b: b_val, cr: cr_val, ct: ct_val}).evalf()
    thickness_ratio_val = thickness_ratio_expr.subs(
        {t: t_val, cr: cr_val}).evalf()
    term1 = Term1_expr.subs(
        {DN: DN_val, AR: AR_val, tr: thickness_ratio_val, G: G_val}).evalf()
    term2 = Term2_expr.subs({ct: ct_val, cr: cr_val}).evalf()
    term3 = (Term3_expr_SI if unit_system == 'SI' else Term3_expr_Imperial).subs(
        {P: pressure, T: temperature}).evalf()

    # Compute flutter velocity
    try:
        print(speed_of_sound)
        print(G_val)
        print(term1)
        print(term2)
        print(term3)
        flutter_velocity = flutter_velocity_function[unit_system](
            speed_of_sound,G_val, term1, term2, term3)
    except Exception as e:
        print(f"Error in computing flutter velocity: {e}")
        flutter_velocity = None
    # Printing expressions and their values
    print("Expressions and their evaluated values:")
    print(f"S = {S_expr.subs({cr: cr_val, ct: ct_val, b: b_val})}")
    print(f"AR = {AR_val}")
    print(
        f"lambda = {lambda_expr.subs({ct: ct_val, cr: cr_val})}")
    print(
        f"t/cr =  {thickness_ratio_expr.subs({t: t_val, cr: cr_val})}")
    print(f"cx = {cx_val}")
    print(f"DN = {DN_val}")
    print(
        f"epsilon = {epsilon_val}")
    print(
        f"Temperature = {T_expr_SI if unit_system == 'SI' else T_expr_Imperial} = {temperature}")
    print(
        f"Pressure = {P_expr_SI if unit_system == 'SI' else P_expr_Imperial} = {pressure}")
    print(
        f"Speed of Sound = {a_expr_SI if unit_system == 'SI' else a_expr_Imperial} = {speed_of_sound}")
    print(f"Term1 = {term1}")
    print(f"Term2 =  = {term2}")
    print(f"Term3 = {Term3_expr_SI if unit_system == 'SI' else Term3_expr_Imperial} = {term3}")
    print(
        f"Flutter Velocity Expression: {Vf_expr_SI if unit_system == 'SI' else Vf_expr_Imperial}")
    print(
        f"Flutter Velocity: {flutter_velocity} {'m/s' if unit_system == 'SI' else 'ft/s'}")


if __name__ == "__main__":
    main()  # Change to "SI" for SI units
