from sympy import symbols, lambdify, sqrt, exp, pi, cos
import numpy as np
import math
import triangle as tr

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
Term1_expr = (DN_expr * AspectRatio_expr**3) / (ThicknessRatio_expr**3 * (AspectRatio_expr + 2))
Term2_expr = (Lambda_expr + 1)/2
Term3_expr = airP / airP  # Assuming sea-level pressure for simplicity
Vf_expr = Spd_of_Sound * sqrt(GE/(Term1_expr * Term2_expr * Term3_expr))

# Lambdify expressions for numerical calculations
fin_area_and_cx_function = lambdify((fin_area, fin_Cx), (fin_area, fin_Cx), modules='numpy')
flutter_velocity_function = lambdify((airP, Temp, Spd_of_Sound, GE, RC, Height, TC, Thickness, fin_Cx), Vf_expr, modules='numpy')


def read_vertex_file(file_name):
    # Read and process the vertex file
    verts = np.genfromtxt(file_name, delimiter=",")
    verts = np.delete(verts, 0, 0)  # Remove header row
    verts = np.delete(verts, 2, 1)  # Remove extra column
    segs = [[i, i+1 if i < len(verts)-1 else 0] for i in range(len(verts))]
    tr_input = dict(vertices=verts, segments=segs)
    tr_output = tr.triangulate(tr_input, 'p')
    return tr_output['triangles'].tolist(), verts


def calculate_triangle_areas_and_cxs(vertices):
    # Code to calculate areas and center of pressure for each triangle
    # for each generated triangle, compute an area and a Cx
    tri_areas = []      # this list will hold the area of each triangle
    tri_Cxs = []        # this list will hold the Cx of each triangle
    fin_area = 0
    fin_Cx = 0
    for tri in tris:		# for every generated triangle
        A = verts[tri[0]]   # extract the vertices of this triangle
        B = verts[tri[1]]
        C = verts[tri[2]]
        # compute triangle area; 0 is index of vertex x coord; 1 is index of vertex y coord
        ar = ((A[0]*(B[1]-C[1])) + (B[0]*(C[1] - A[1])) + (C[0]*(A[1] - B[1])))/2
        # add the area of this triangle to our list of areas
        tri_areas.append(ar)
        fin_area += ar          # add the area of this triangle to the total fin area
        # compute triangle Cx; 0 is the index of the vertex x coord
        tri_Cx = (A[0] + B[0] + C[0]) / 3
        tri_Cxs.append(tri_Cx)  # add the Cx of this triangle to our list of Cx's
    # compute Fin Cx by taking the weighted average of all of the triangle Cx's
    for i in range(len(tri_areas)):  # first get the numerator (weighted sum of areas)
        fin_Cx += (tri_Cxs[i] * tri_areas[i])
    fin_Cx = (fin_Cx / fin_area)     # now divide by the total fin area to get Cx

    # Compute Vf; first compute all intermediate values
    Fin_Eps = (fin_Cx / RC) - 0.25  # compute epsilon (see article for definition)
    

def calculate_fin_area_and_cx(fin_area_val, fin_cx_val):
    """
    Calculate the fin area and center of pressure.
    """
    return fin_area_and_cx_function(fin_area_val, fin_cx_val)


def calculate_flutter_velocity(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, center_of_pressure):
    """
    Calculate the flutter velocity of a fin.
    """
    return flutter_velocity_function(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, center_of_pressure)

# Example usage of the functions:
# Assuming you have the values for fin_area_val, fin_cx_val, air_pressure, etc.
# fin_area_val, fin_cx_val = calculate_fin_area_and_cx(...)
# flutter_velocity = calculate_flutter_velocity(air_pressure, temperature, speed_of_sound, shear_modulus, root_chord, height, tip_chord, thickness, fin_cx_val)