from sympy import symbols, lambdify, N
import numpy as np

# Define symbols
cr, ct, b, h, T, G, t, P, m, K, P0 = symbols('c_r c_t b h T G t P m K P0')

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
DN_expr = (24*epsilon_expr*K*P0)/np.pi
Term1_expr = (DN_expr*AR_expr**3)/((thickness_ratio_expr**3)*(AR_expr+2))
Term2_expr = (lambda_expr+1)/2
Vf_expr_Imperial = a_expr_Imperial * (G / (Term1_expr * Term2_expr * Term3_expr_Imperial))**0.5
Vf_expr_SI = a_expr_SI * (G / (Term1_expr * Term2_expr * Term3_expr_SI))**0.5

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
flutter_velocity_function = {
    "SI": lambdify((G, cr, ct, b, t, m, P, K, P0, T), Vf_expr_SI, modules='numpy'),
    "Imperial": lambdify((G, cr, ct, b, t, m, P, K, P0, T), Vf_expr_Imperial, modules='numpy')
}

# Main function
def main(unit_system):
    # Input parameters
    cr_val = 7.5  # inch or cm based on unit system
    ct_val = 2.5  # inch or cm
    b_val = 3.0  # inch or cm
    h_val = 4500.0 + 14000.0  # ft or meters
    t_val = 0.1875  # inch or cm
    m_val = 4.285  # inch or cm
    G_val = 600000.0  # psi or kPa
    K_val = 1.4  # constant
    P0_val = 14.696 if unit_system == "Imperial" else 101.325  # psi or kPa

    # Compute intermediate values
    temperature = temperature_function[unit_system](h_val)
    pressure = pressure_function[unit_system](temperature)
    speed_of_sound = speed_of_sound_function[unit_system](temperature)

    # Compute flutter velocity
    flutter_velocity = flutter_velocity_function[unit_system](
        G_val, cr_val, ct_val, b_val, t_val, m_val, pressure, K_val, P0_val, temperature)

    print(f"Temperature: {temperature} {'Fahrenheit' if unit_system == 'Imperial' else 'Celsius'}")
    print(f"Pressure: {pressure} {'psi' if unit_system == 'Imperial' else 'kPa'}")
    print(f"Speed of Sound: {speed_of_sound} {'ft/s' if unit_system == 'Imperial' else 'm/s'}")
    print(f"Flutter Velocity: {flutter_velocity} {'ft/s' if unit_system == 'Imperial' else 'm/s'}")

if __name__ == "__main__":
    main("Imperial")  # Change to "SI" for SI units
