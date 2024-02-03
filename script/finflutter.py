import numpy as np
import matplotlib.pyplot as plt

class FinFlutter:
    """
    A class to calculate fin flutter characteristics for aerospace applications.

    This class supports calculations in both SI and Imperial units. It provides methods to calculate
    fin flutter speed using two different equations, one based on SI units and another based on Imperial units.

    Attributes:
        altitude (float) (ft or m): Altitude at which the fin operates.
        shear_modulus (float) (Pa or ...): Shear modulus of the fin material.
        root_chord (float) (m or inches): Root chord length of the fin.
        tip_chord (float) (m or inches): Tip chord length of the fin.
        semi_span (float) (m or inches): Semi-span of the fin.
        speed_of_sound (float): Speed of sound at the given altitude.
        atmospheric_height (float): Scale height of the atmosphere.
        std_atm_pressure (float): Standard atmospheric pressure.
        temperature (float): Temperature at the given altitude.
        pressure (float): Pressure at the given altitude.
    """    
    
    
    def __init__(self, shear_modulus: float, root_chord: float, tip_chord: float, semi_span: float, altitude: int = 10000, speed_of_sound: float = 335, atmospheric_height: float = 8077, std_atm_pressure: float = 101325):
        self.altitude = altitude
        self.shear_modulus = shear_modulus
        self.speed_of_sound = speed_of_sound
        self.atmospheric_height = atmospheric_height
        self.std_atm_pressure = std_atm_pressure
        # self.temperature = 0
        # self.pressure = 0

        # self.semi_span = semi_span / 1000  # Convert mm to meters
        # self.tip_chord = tip_chord / 1000  # Convert mm to meters
        # self.root_chord = root_chord / 1000  # Convert mm to meters

        self.semi_span = semi_span
        self.tip_chord = tip_chord
        self.root_chord = root_chord

    def set_temperature(self, temperature: float) -> None:
        """set_temperature  Set the temperature of the fin.

        :param temperature:  The temperature of the fin.
        :type temperature: float
        """
        self.temperature = temperature

    def set_pressure(self, pressure: float) -> None:
        """set_pressure  Set the pressure of the fin.

        :param pressure:  The pressure of the fin.
        :type pressure: float
        """
        self.pressure = pressure

    def set_altitude(self, altitude: float) -> None:
        """set_altitude  Set the altitude of the fin.

        :param altitude:  The altitude of the fin.
        :type altitude: float
        """
        self.alitide = altitude

    def set_shear_modulus(self, shear_modulus: float) -> None:
        """set_shear_modulus  Set the shear modulus of the fin.

        :param shear_modulus:  The shear modulus of the fin.
        :type shear_modulus: float
        """
        self.shear_modulus = shear_modulus

    def set_thickness(self, thickness: float) -> None:
        """set_thickness  Set the thickness of the fin.

        :param thickness: The thickness of the fin.
        :type thickness: float
        """
        self.thickness = thickness

    def set_speed_of_sound(self, speed_of_sound: float) -> None:
        """set_speed_of_sound  Set the speed of sound of the fin.

        :param speed_of_sound:  The speed of sound of the fin.
        :type speed_of_sound: float
        """
        self.speed_of_sound = speed_of_sound

    def set_atmospheric_height(self, atmospheric_height: float) -> None:
        """set_atmospheric_height  Set the atmospheric height of the fin.

        :param atmospheric_height:  The atmospheric height of the fin.
        :type atmospheric_height: float
        """
        self.atmospheric_height = atmospheric_height

    def set_std_atm_pressure(self, std_atm_pressure: float) -> None:
        """set_std_atm_pressure  Set the standard atmospheric pressure of the fin.

        :param std_atm_pressure:  The standard atmospheric pressure of the fin.
        :type std_atm_pressure: float
        """
        self.std_atm_pressure = std_atm_pressure

    def set_semi_span(self, semi_span: float) -> None:
        """set_semi_span  Set the semi span of the fin.

        :param semi_span:  The semi span of the fin.
        :type semi_span: float
        """
        self.semi_span = semi_span

    def set_tip_chord(self, tip_chord: float) -> None:
        """set_tip_chord  Set the tip chord of the fin.

        :param tip_chord:  The tip chord of the fin.
        :type tip_chord: float
        """
        self.tip_chord = tip_chord

    @property
    def wing_area(self) -> float:
        """wing_area  Returns the wing area of the fin.

        :return:  The wing area of the fin.
        :rtype: float
        """
        wing_area = 0.5*(self.root_chord+self.tip_chord)*self.semi_span
        return wing_area

    @property
    def aspect_ratio(self) -> float:
        """aspect_ratio  Returns the aspect ratio of the fin.

        :return:  The aspect ratio of the fin.
        :rtype: float
        """
        aspect_ratio = np.power(self.semi_span, 2)/self.wing_area
        return aspect_ratio

    @property
    def taper_ratio(self) -> float:
        """taper_ratio  Returns the taper ratio of the fin.

        :return:  The taper ratio of the fin.
        :rtype: float
        """
        taper_ratio = self.tip_chord/self.root_chord
        return taper_ratio

    @property
    def temperature(self) -> float:
        """temperature  Returns the temperature of the fin.

        :return:  The temperature of the fin.
        :rtype: float
        """
        return 59 - 0.00356*self.altitude

    @property
    def pressure(self) -> float:
        """pressure  Returns the pressure of the fin in lbs/ft^2.

        :return:  The pressure of the fin.
        :rtype: float
        """

        return (2116/144) * np.float_power(((self.temperature + 459.7)/518.6), 5.256)

    def calc_speed_of_sound(self) -> float:
        """calc_speed_of_sound  Calcualte the speed of sound based on Zachary Howard. “How To Calculate Fin Flutter Speed”. In: Peak of Flight 291 (July 2011).

        :return:  speed of sound 
        :rtype: float
        """
        speed_of_sound = np.sqrt(1.4*1716.59*(self.temperature+460))
        return speed_of_sound

    def calculate_flutter_velocity_eq2(self, thickness: float) -> float:
        """calculate_flutter_velocity_eq2  Calculate the fin flutter based on Zachary Howard. “How To Calculate Fin Flutter Speed”. In: Peak of Flight 291 (July 2011).

        :param thickness:  The thickness of the fin in inches
        :type thickness: float
        :return:  Fin flutter in mph
        :rtype: float
        """
        bottom_denominator = 2*(self.aspect_ratio + 2) * \
            np.power((thickness/self.root_chord), 3)

        middle_part = 1.337 * \
            np.power(self.aspect_ratio, 3) * \
            self.pressure * (self.taper_ratio + 1)

        flutter_velocity = self.calc_speed_of_sound()*np.sqrt(self.shear_modulus /
                                                              (middle_part/bottom_denominator))
        return flutter_velocity

    def normalised_thickness(self, thickness: float) -> float:
        """normalised_thickness  Returns the normalised thickness of the fin.

        :param thickness:  The thickness of the fin.
        :type thickness:  float
        :return:  The normalised thickness of the fin.
        :rtype: float
        """
        normalised_thickness = (thickness/1000)/self.root_chord
        return normalised_thickness

    def calculate_flutter_velocity(self, thickness: float) -> float:
        """calculate_flutter_velocity  Calculates the flutter velocity of the fin based on a given thickness.

        :param thickness:  The thickness of the fin.
        :type thickness: float
        :return:  The flutter velocity of the fin.
        :rtype: float
        """
        # Debug print statements to check intermediate values
        exponent_part = np.exp(0.4 * self.altitude / self.atmospheric_height)
        first_sqrt_part = np.sqrt(self.shear_modulus/self.std_atm_pressure)
        second_sqrt_part = np.sqrt((2 + self.aspect_ratio) /
                                   (1 + self.taper_ratio))
        bracket_part = np.power(self.normalised_thickness(
            thickness)/self.aspect_ratio, 3/2)
        flutter_velocity = 1.223 * self.speed_of_sound * exponent_part * \
            first_sqrt_part * second_sqrt_part * bracket_part
        return flutter_velocity

    def calculate_thickess(self, flutter_velocity: float) -> float:
        """calculate_thickess  Calculates the thickness of the fin based on a given flutter velocity.

        :param flutter_velocity:  The flutter velocity of the fin.
        :type flutter_velocity: float
        :return:  The thickness of the fin.
        :rtype: float
        """
        first_exponent_part = np.exp(
            0.4 * self.altitude / self.atmospheric_height)
        first_sqrt_part = np.sqrt(self.shear_modulus/self.std_atm_pressure)
        second_sqrt_part = np.sqrt((2 + self.aspect_ratio) /
                                   (1 + self.taper_ratio))

        inside_exponent = 1.223 * self.speed_of_sound * first_exponent_part * \
            first_sqrt_part * second_sqrt_part

        overall_exponent = np.power(flutter_velocity/inside_exponent, 2/3)

        normalised_thickness = (overall_exponent*self.aspect_ratio)
        thickness = normalised_thickness * self.root_chord * 1000
        return thickness

    def calculate_safety_factor(self, design_thickness: float, max_allowable_velocity: float) -> float:
        """
        Calculate the safety factor for a given thickness.

        Safety Factor = Max Allowable Velocity / Calculated Flutter Velocity

        :param design_thickness: Design thickness of the fin (in mm).
        :param max_allowable_velocity: Maximum allowable flutter velocity (in m/s).
        :return: Safety factor.
        """
        design_flutter_velocity = self.calculate_flutter_velocity(
            design_thickness)
        if max_allowable_velocity == 0:
            return float('inf')  # To avoid division by zero
        return design_flutter_velocity / max_allowable_velocity

    def print_summary(self) -> None:
        """print_summary  Prints a summary of the fin.
        """
        print(f"Altitude: {self.altitude}")
        print(f"Shear modulus: {self.shear_modulus}")
        print(f"Standard atmospheric pressure: {self.std_atm_pressure}")

        print("\n")
        print(f"Root Chord: {self.root_chord}")
        print(f"Tip Chord: {self.tip_chord}")
        print(f"Aspect ratio: {self.aspect_ratio}")
        print(f"Taper ratio: {self.taper_ratio}")
        print(f"Semi Span: {self.semi_span}")
        # print(f"Thickness: {thickness}")
        # print(f"Normalised Thickness: {self.normalised_thickness(thickness)}")

        print("\n")
        print(f"Speed of sound: {self.speed_of_sound}")
        print(f"Atmospheric height: {self.atmospheric_height}")

    def plot_flutter_velocity(self, max_thickness: float, thickness_increments: float, design_thickness=None, max_velocity=None):
        thickness_list = np.arange(
            0, max_thickness + thickness_increments, thickness_increments)
        flutter_velocity_list = [self.calculate_flutter_velocity(
            thickness) for thickness in thickness_list]

        fig, ax1 = plt.subplots(figsize=(12, 6))

        ax1.set_xlabel('Thickness (mm)')
        ax1.set_ylabel('Flutter Velocity (m/s)', color='tab:blue')
        ax1.plot(thickness_list, flutter_velocity_list,
                 label='Flutter Velocity', marker='o', color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Add max rocket velocity horizontal line and set it as safety factor of 1
        if max_velocity is not None:
            ax1.axhline(y=max_velocity, color='purple', linestyle='--',
                        linewidth=2, label=f'Max Rocket Velocity: {max_velocity}m/s')

        # Set up the second y-axis for the safety factor
        ax2 = ax1.twinx()
        ax2.set_ylabel('Safety Factor', color='tab:red')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        # # Since max_velocity corresponds to a safety factor of 1, we set the max velocity line here
        # if max_velocity is not None:
        #     # No label needed, as it's the same line
        #     ax2.axhline(y=1, color='purple', linestyle='--', linewidth=2)

        # Rescale the safety factor axis based on the max_velocity
        # Set the top limit to maintain the 1 ratio
        ax2.set_ylim(bottom=0, top=max(flutter_velocity_list) / max_velocity)

        # Highlight design thickness and max thickness points if provided
        if design_thickness is not None:
            design_velocity = self.calculate_flutter_velocity(design_thickness)
            design_safety_factor = self.calculate_safety_factor(
                design_thickness, max_velocity)
            ax1.axvline(x=design_thickness, color='red', linestyle='--',
                        linewidth=2, label=f'Design Thickness: {design_thickness}mm')
            ax2.axhline(y=design_safety_factor, color='orange', linestyle='-.',
                        linewidth=2, label=f'Design Safety Factor: {design_safety_factor:.2f}')

        if max_velocity is not None:
            max_thickness_value = self.calculate_thickess(max_velocity)
            ax1.axvline(x=max_thickness_value, color='green', linestyle='--',
                        linewidth=2, label=f'Max Thickness: {max_thickness_value:.2f}mm')

        plt.title('Fin Flutter Analysis', y=1.05)
        ax1.legend(loc='upper left')
        fig.tight_layout()
        plt.grid(True)
        plt.show()

    def evaluate_flutter_design(self, design_thickness: float, max_velocity: float) -> None:
        """
        Evaluates the flutter design based on the given design thickness and maximum velocity.

        Parameters:
        design_thickness (float): The thickness of the design in millimeters.
        max_velocity (float): The maximum velocity of the rocket in meters per second.
        """
        # Calculate flutter velocity for design thickness
        design_flutter_velocity = self.calculate_flutter_velocity(
            design_thickness)
        print(f"Design Flutter Velocity: {design_flutter_velocity:.2f} m/s")

        # Check if design flutter velocity is bigger than max velocity
        if design_flutter_velocity > max_velocity:
            print("The design is safe.")
        else:
            print("The design is not safe. Adjust thickness.")

        # Call the extended plotting function
        self.plot_flutter_velocity(
            max_thickness=8, thickness_increments=0.1, design_thickness=design_thickness, max_velocity=max_velocity)


def main():
    # Create an instance of FinFlutter with the required parameters
    # Create an instance of FinFlutter with the required parameters
    # fin_flutter = FinFlutter(
    #     altitude=3048,
    #     shear_modulus=5e9,
    #     root_chord=300,
    #     tip_chord=100,
    #     semi_span=140,
    #     speed_of_sound=346.06  # Example speed of sound
    # )

    # # User input for design thickness and max velocity
    # design_thickness = float(input("Enter design thickness (in mm): "))
    # max_velocity = float(input("Enter max rocket velocity (in m/s): "))

    # fin_flutter.evaluate_flutter_design(design_thickness, max_velocity)

    news_fin = FinFlutter(altitude=3000, shear_modulus=380000,
                          root_chord=9.75, tip_chord=3.75, semi_span=4.75)

    fin_flutter_velocity = news_fin.calculate_flutter_velocity_eq2(0.125)

    news_fin.print_summary()
    print('\n')
    print(f"fin flutter (ft/sec)= {fin_flutter_velocity}")


if __name__ == "__main__":
    main()
