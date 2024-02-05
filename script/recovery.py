import math
import numpy as np


class RocketParachuteCalculator:
    GRAVITY = 9.81

    def calc_area_cd(self, safety_factor: float, rocket_mass: float, air_density: float, descent_velocity: float) -> float:
        """
        Calculate the area coefficient of drag for a parachute.

        The formula used is:
        area_cd = safety_factor * (2 * rocket_mass * GRAVITY) / (air_density * descent_velocity ** 2)

        Parameters:
        - safety_factor: A multiplier to ensure the parachute is overdesigned for safety.
        - rocket_mass: Mass of the rocket.
        - air_density: Density of the air where the parachute will be deployed.
        - descent_velocity: The desired velocity of the rocket during descent.

        Returns:
        - The calculated area coefficient of drag.
        """
        return safety_factor * (2 * rocket_mass * self.GRAVITY) / (air_density * descent_velocity ** 2)

    def calc_gore_panel_side_length(self, area_cd: float, hole_to_canopy_area_ratio: float, drag_coefficient: float, number_of_gores_panels: int) -> float:
        """
        Calculate the side length of a gore panel in a parachute.

        The formula used is:
        side_length = 2 * ((math.pi * area_cd / (1 - hole_to_canopy_area_ratio) / drag_coefficient) ** 0.5) / number_of_gores_panels

        Parameters:
        - area_cd: The area coefficient of drag, output from calc_area_cd.
        - hole_to_canopy_area_ratio: Ratio defining the size of the hole in the parachute to its overall area.
        - drag_coefficient: The drag coefficient of the parachute material.
        - number_of_gores_panels: The number of gore panels in the parachute.

        Returns:
        - The side length of each gore panel.
        """
        return 2 * ((math.pi * area_cd / (1 - hole_to_canopy_area_ratio) / drag_coefficient) ** 0.5) / number_of_gores_panels

    def calc_circumference(self, area_cd: float, hole_to_canopy_area_ratio: float, drag_coefficient: float) -> float:
        """
        Calculate the circumference of the parachute directly from the area coefficient of drag,
        the hole to canopy area ratio, and the drag coefficient.

        The simplified formula used is:
        circumference = 2 * ((math.pi * area_cd / (1 - hole_to_canopy_area_ratio) / drag_coefficient) ** 0.5)

        Parameters:
        - area_cd: The area coefficient of drag, output from calc_area_cd.
        - hole_to_canopy_area_ratio: Ratio defining the size of the hole in the parachute to its overall area.
        - drag_coefficient: The drag coefficient of the parachute material.

        Returns:
        - The circumference of the parachute.
        """
        return 2 * ((math.pi * area_cd / (1 - hole_to_canopy_area_ratio) / drag_coefficient) ** 0.5)

    def calc_radius(self, circumference: float) -> float:
        """
        Calculate the radius of the parachute based on its circumference.

        The formula used is:
        radius = circumference / (2 * math.pi)

        Parameters:
        - circumference: The circumference of the parachute.

        Returns:
        - The radius of the parachute.
        """
        return circumference / (2 * math.pi)

    def calc_circular_area(self, area_cd: float, drag_coefficient: float, hole_to_canopy_area_ratio: float) -> float:
        """
        Calculate the circular area of a selected section of the parachute.

        The formula used is:
        circular_area_of_selected = area_cd / drag_coefficient / (1 - hole_to_canopy_area_ratio)

        Parameters:
        - area_cd: The area coefficient of drag, output from calc_area_cd.
        - drag_coefficient: The drag coefficient of the parachute material.
        - hole_to_canopy_area_ratio: Ratio defining the size of the hole in the parachute to its overall area.

        Returns:
        - The circular area of the selected parachute section in square meters.
        """
        return area_cd / drag_coefficient / (1 - hole_to_canopy_area_ratio)

    def calc_circular_diameter(self, circular_area_of_selected: float):
        return math.sqrt(4*circular_area_of_selected/math.pi)

    def calc_ellipse_perimeter(self, a: float, b: float, terms: int = 10) -> float:
        """
        Calculate the perimeter of an ellipse using an infinite series approximation.

        The formula used is:
        p = π(a + b) * Σ((0.5/n)^2 * h^n) from n=0 to infinity

        Here the series is approximated by summing up to 'terms' number of terms.

        Parameters:
        - a: Semi-major axis of the ellipse.
        - b: Semi-minor axis of the ellipse.
        - terms: Number of terms to include in the summation for the approximation.

        Returns:
        - The approximate perimeter of the ellipse.
        """
        h = ((a - b)**2) / ((a + b)**2)
        sum_series = sum(((0.5 / n)**2 * (h**n) for n in range(1, terms + 1)))
        perimeter = math.pi * (a + b) * (1 + sum_series)
        return perimeter

    def calc_semi_ellipsoid_depth(self, radius, ratio_of_height_to_radius):
        np_radius = np.array(radius)
        np_ratio_of_height_to_radius = np.array(ratio_of_height_to_radius)
        depth = np.outer(np_radius, np_ratio_of_height_to_radius)
        return depth[0]

    def calc_length_of_curve(self, radius, semi_ellipsoid_depth, length_to_half_circumference_ratio):
        """
        Calculate the length of the curve using an approximation formula by Ramanujan.

        Ramanujan's approximation for the circumference (p) of an ellipse with semi-major axis (a) and
        semi-minor axis (b) is given by:

            p ≈ π [ 3(a + b) - sqrt{ (3a + b)(a + 3b) } ]

        https://www.mathsisfun.com/geometry/ellipse-perimeter.html

        In this context, 'a' is the radius of the base of the semi-ellipsoid, 'b' is the depth of the
        semi-ellipsoid, and the resulting length of the curve is a quarter of the total circumference
        multiplied by a ratio factor.

        Parameters:
        - radius: The radius of the base of the semi-ellipsoid (semi-major axis 'a').
        - semi_ellipsoid_depth: The depth of the semi-ellipsoid (semi-minor axis 'b').
        - length_to_half_circumference_ratio: Ratio for calculating the length to the half circumference.

        Returns:
        - The length of the curve, which is a quarter of the ellipse's circumference adjusted by the
        length to half circumference ratio.
        """
        length_of_curve = 0.25 * length_to_half_circumference_ratio * \
            np.pi * (3 * (radius + semi_ellipsoid_depth) -
                     np.sqrt((3 * radius + semi_ellipsoid_depth) * (radius + 3 * semi_ellipsoid_depth)))
        return length_of_curve

    def calc_length_of_curve_without_hole(self, length_of_curve, hole_to_canopy_area_ratio):
        return length_of_curve*(1-hole_to_canopy_area_ratio)

    def calc_material_area_per_gore(self, side_length: float, length_of_curve_without_hole: float):
        return 2*side_length*length_of_curve_without_hole/math.pi
    
    def calc_material_area_per_chute(self,number_of_gores_panels:float,material_area_per_gore:float):
        return number_of_gores_panels*material_area_per_gore
    
    def calc_material_area_for_net(self,number_of_gores_panels:float,length_of_curve_without_hole,side_length):
        return number_of_gores_panels*length_of_curve_without_hole*side_length
    
    def calc_mass_per_chute(self,material_area_per_chute,mass_per_unit_area):
        return material_area_per_chute*mass_per_unit_area
    
    def calc_cost_per_chute(self,material_area_for_net,cost_per_unit_area):
        return material_area_for_net*cost_per_unit_area
