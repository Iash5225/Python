from sympy import symbols, lambdify, sqrt, exp, pi, cos
import numpy as np
import math
import triangle as tr

# Define symbols
MaxV, AMaxV, LSA, TLS, DEF, Thickness, TC, RC, Height, GE, T2T, fin_area, fin_Cx = symbols(
    'MaxV AMaxV LSA TLS DEF Thickness TC RC Height GE T2T fin_area fin_Cx')
airP, Temp, Spd_of_Sound, Term1, Term2, Term3, Vf = symbols(
    'airP Temp Spd_of_Sound Term1 Term2 Term3 Vf')

# Define additional symbols
p0, DST_Base_Temp, Temp_Dec_Per_Unit, SoS_Mult, Low_Temp, T0, Fin_Eps, ThicknessRatio, Lambda, AspectRatio, DN, Temp, Margin, Margin_Pct = symbols(
    'p0 DST_Base_Temp Temp_Dec_Per_Unit SoS_Mult Low_Temp T0 Fin_Eps ThicknessRatio Lambda AspectRatio DN Temp Margin Margin_Pct')

# Expressions for Fin Area and Center of Pressure (Cx)
# These would be computed from the given fin vertex data
# For now, let's assume they are inputs

Fin_Eps_expr = (fin_Cx / RC) - 0.25
ThicknessRatio_expr = Thickness / RC
Lambda_expr = TC / RC
AspectRatio_expr = Pow(Height, 2) / fin_area
DN_expr = (24 * Fin_Eps_expr * 1.4 * p0) / pi
Temp_expr = DST_Base_Temp - (Temp_Dec_Per_Unit * (LSA + AMaxV)
                             ) if DEF == "DST" else TLS - (Temp_Dec_Per_Unit * AMaxV)
Spd_of_Sound_expr = SoS_Mult * sqrt(Low_Temp + Temp_expr)
airP_expr = p0 * Pow(((Temp_expr + Low_Temp) / T0), 5.256)
Term1_expr = (DN_expr * Pow(AspectRatio_expr, 3)) / \
    (Pow(ThicknessRatio_expr, 3) * (AspectRatio_expr + 2))
Term2_expr = (Lambda_expr + 1) / 2
Term3_expr = airP_expr / p0
Vf_expr = Spd_of_Sound_expr * sqrt(GE / (Term1_expr * Term2_expr * Term3_expr))
Margin_expr = Vf_expr - MaxV
Margin_Pct_expr = 100 * ((Vf_expr - MaxV) / MaxV)

# Lambdify expressions for numerical calculations
fin_area_and_cx_function = lambdify(
    (fin_area, fin_Cx), (fin_area, fin_Cx), modules='numpy')
flutter_velocity_function = lambdify(
    (airP, Temp, Spd_of_Sound, GE, RC, Height, TC, Thickness, fin_Cx), Vf_expr, modules='numpy')
# Lambdify the new expressions
calculate_terms_function = lambdify((fin_Cx, RC, TC, Height, fin_area, p0, DEF, LSA, AMaxV, DST_Base_Temp, Temp_Dec_Per_Unit, TLS, SoS_Mult, Low_Temp, T0, Thickness, GE, airP), (
    Fin_Eps_expr, ThicknessRatio_expr, Lambda_expr, AspectRatio_expr, DN_expr, Temp_expr, Spd_of_Sound_expr, airP_expr, Term1_expr, Term2_expr, Term3_expr, Vf_expr, Margin_expr, Margin_Pct_expr), modules='numpy')


def read_vertex_file(file_name):
    # Read and process the vertex file
    verts = np.genfromtxt(file_name, delimiter=",")
    verts = np.delete(verts, 0, 0)  # Remove header row
    verts = np.delete(verts, 2, 1)  # Remove extra column
    segs = [[i, i+1 if i < len(verts)-1 else 0] for i in range(len(verts))]
    tr_input = dict(vertices=verts, segments=segs)
    tr_output = tr.triangulate(tr_input, 'p')
    return tr_output['triangles'].tolist(), verts


def calculate_triangle_areas_and_cxs(triangles, verts):
    tri_areas = []
    tri_Cxs = []
    fin_area = 0
    fin_Cx = 0
    for tri in triangles:
        A, B, C = [verts[i] for i in tri]
        area = ((A[0]*(B[1]-C[1])) + (B[0]*(C[1] - A[1])) +
                (C[0]*(A[1] - B[1]))) / 2
        tri_areas.append(area)
        fin_area += area
        tri_Cx = (A[0] + B[0] + C[0]) / 3
        tri_Cxs.append(tri_Cx)
        fin_Cx += tri_Cx * area
    fin_Cx /= fin_area
    return fin_area, fin_Cx, tri_areas, tri_Cxs


def calculate_flutter_velocity(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, center_of_pressure):
    """
    Calculate the flutter velocity of a fin.
    """
    return flutter_velocity_function(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, center_of_pressure)

# Example usage of the functions:
# Assuming you have the values for fin_area_val, fin_cx_val, air_pressure, etc.
# fin_area_val, fin_cx_val = calculate_fin_area_and_cx(...)
# flutter_velocity = calculate_flutter_velocity(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, fin_cx_val)


def main():
    # Assume default values for parameters
    # These should be replaced by actual values where necessary
    units = "SI"
    maxv = 457.2  # Example value
    amaxv = 4267.2  # Example value
    lsa = 1371.6  # Example value
    tls = 18.333  # Example value
    thickness = 0.47625  # Example value
    tc = 6.35  # Example value
    rc = 19.05  # Example value
    height = 7.62  # Example value
    ge = 4136854  # Example value
    t2t = "YES"  # Example value
    fin_vertex_file_name = "trap_SI.csv"  # Example value

    # Example usage
    triangles, verts = read_vertex_file(fin_vertex_file_name)
    fin_area_val, fin_cx_val, _, _ = calculate_triangle_areas_and_cxs(triangles, verts)


        # Define additional parameters based on the units
    if units == "Imperial":
        p0_val = 14.696
        dst_base_temp_val = 59
        temp_dec_per_unit_val = 0.00356
        sos_mult_val = 49.03
        low_temp_val = 459.7
        t0_val = 518.7
    else:
        p0_val = 101.325
        dst_base_temp_val = 15
        temp_dec_per_unit_val = 0.0065
        sos_mult_val = 20.05
        low_temp_val = 273.16
        t0_val = 288.16

    # Calculate additional terms
    terms = calculate_terms_function(fin_cx_val, rc, tc, height, fin_area_val, p0_val, "DST", lsa, amaxv,
                                    dst_base_temp_val, temp_dec_per_unit_val, tls, sos_mult_val, low_temp_val, t0_val, thickness, ge, airP)
    fin_eps, thickness_ratio, lambda_val, aspect_ratio, dn, temp_val, spd_of_sound, airp, term1, term2, term3, vf, margin, margin_pct = terms

# Output the results


if __name__ == "__main__":
    main()  # Replace with your file path


Fix it so it calculates flutter velocity