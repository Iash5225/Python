import pandas as pd
import re
import math


class DataHandler:
    """Handles data operations for rocket analysis."""

    def __init__(self, or_filepath: str = "", ras_cd_filepath: str = "", ras_file_path: str = ""):
        """
        __init__  Initializes the DataHandler class with a given file path.

        :param or_filepath:  Filepath to the OR rocket exported CSV file
        :type or_filepath: str 
        """
        self.or_filepath = or_filepath
        self.ras_cd_filepath = ras_cd_filepath
        self.ras_file_path = ras_file_path
        self.df = None
        self.comments_df = None
        self.merged_df = None
        self.filtered_or_df = None
        self.ras_df = None
        self.ras_mach_df = None
        self.filtered_ras_df = None
        self.max_RAS_mach = 2.0
        self._prepare_dataframes()

    def set_max_RAS_mach(self, max_mach: float) -> None:
        """
        set_max_RAS_mach   Sets the maximum Mach number for the RAS Aero CSV file.

        :param max_mach:  Maximum Mach number
        :type max_mach: float
        """
        self.max_RAS_mach = max_mach

    def _read_OR_csv(self) -> None:
        """
        _read_OR_csv  Reads the Open Rocket CSV file and stores it in a DataFrame.
        """
        try:
            self.df = pd.read_csv(self.or_filepath, delimiter=",", skiprows=6)
        except Exception as e:
            print(f"Error reading the OR CSV file: {e}")

    def _read_RASAero_Mach_csv(self) -> None:
        """
        _read_RASAero_Mach_csv  Reads the RAS Aero Mach CSV file and stores it in a Dataframe.
        """
        try:
            self.ras_mach_df = pd.read_csv(self.ras_cd_filepath)
        except Exception as e:
            print(f"Error reading the RAS CSV file: {e}")

    def _read_RASAero_csv(self) -> None:
        """
        _read_RASAero_csv  Reads the RasAero CSV file and stores it in a Dataframe.
        """
        try:
            self.ras_df = pd.read_csv(self.ras_file_path)
        except Exception as e:
            print(f"Error reading the RAS CSV file: {e}")

    def export_mach_cd_df_to_txt(self, OUTPUT_FILE_PATH: str):
        """
        export_mach_cd_df_to_txt  Exports the Mach and CD DataFrame to a tab-delimited text file.

        :param OUTPUT_FILE_PATH:  Output file path
        :type OUTPUT_FILE_PATH: str
        """

        df = self.filtered_ras_df[["Mach", "CD"]]

        # Export the DataFrame as a tab-delimited text file
        df.to_csv(OUTPUT_FILE_PATH, sep="\t", index=False)

    def _prepare_dataframes(self) -> None:
        """
        _prepare_dataframes  Prepares the dataframes for analysis. These include: initial dataframe, filtered dataframe, comments dataframe, and merged dataframe.
        """
        if self.or_filepath != "":
            self._read_OR_csv()
            self._filter_comments()
            self.filtered_or_df = self._filter_data()
            self.merged_df = self._merge_dataframes()

        if self.ras_cd_filepath != "":
            self._read_RASAero_Mach_csv()
            self.filter_mach_from_ras_csv()

        if self.ras_file_path != "":
            self._read_RASAero_csv()

    def filter_mach_from_ras_csv(self) -> None:
        """
        filter_mach_from_ras_csv  Filters the RAS Aero CSV file by Mach number.
        """
        filtered_RAS_df = self.ras_mach_df[self.ras_mach_df["Mach"]
                                           <= self.max_RAS_mach]
        filtered_RAS_df = filtered_RAS_df.drop_duplicates(subset=['Mach'])
        self.filtered_ras_df = filtered_RAS_df

    def _filter_comments(self) -> None:
        """
        _filter_comments  Filters comments from the main DataFrame and stores them separately.
        """
        comments_mask = self.df["# Time (s)"].astype(str).str.contains("#")
        comments_df = self.df[comments_mask].copy()
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            self._extract_time)
        comments_df["Event"] = comments_df["# Time (s)"].apply(
            self._extract_event)
        self.comments_df = self._process_comment_events(comments_df)

    def _filter_data(self) -> pd.DataFrame:
        """
        _filter_data  Filters out comment rows from the main DataFrame.

        :return:  Filtered DataFrame
        :rtype: pd.DataFrame
        """
        filtered_or_df = self.df[~self.df["# Time (s)"].astype(
            str).str.contains("#")].copy()
        filtered_or_df.rename(columns={"# Time (s)": "Time (s)"}, inplace=True)
        return filtered_or_df

    def _merge_dataframes(self) -> pd.DataFrame:
        """
        _merge_dataframes  Merges the filtered data with the comments data. As well as cleans U+200B characters.

        :return:  Merged DataFrame
        :rtype: pd.DataFrame
        """
        # Convert 'Time (s)' in both dataframes to float
        self.filtered_or_df["Time (s)"] = pd.to_numeric(
            self.filtered_or_df["Time (s)"], errors='coerce')
        if self.comments_df is not None:
            self.comments_df["Time (s)"] = pd.to_numeric(
                self.comments_df["Time (s)"], errors='coerce')

        # Perform the merge
        merged = self.filtered_or_df.merge(
            self.comments_df, on="Time (s)", how="left")

        # Clean U+200B characters from data
        for column in merged.columns:
            if merged[column].dtype == object:
                merged[column] = merged[column].str.replace('\u200b', '')

        # Clean U+200B characters from column names
        merged.columns = [col.replace('\u200b', '') for col in merged.columns]
        return merged

    def _extract_time(self, text: str) -> float:
        """
        _extract_time  Extracts time from a comment string. The string must be in the format: "occurred at t=0.000 seconds"

        :param text:  Comment string
        :type text: str
        :return:  Time in seconds
        :rtype: float
        """
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def _extract_event(self, text: str) -> str:
        """
        _extract_event  Extracts event name from a comment string. The string must be in the format: "occurred at t=0.000 seconds"

        :param text:  Comment string
        :type text: str
        :return:  Event name
        :rtype: str
        """
        return text.replace(r"occurred at t=[\d\.]+ seconds", "").replace("#", "").strip()

    def _process_comment_events(self, comments_df: pd.DataFrame) -> pd.DataFrame:
        """
        _process_comment_events  Processes events in the comments dataframe. This includes removing non-caps words, replacing events, and removing events.

        :param comments_df:  Comments DataFrame
        :type comments_df: pd.DataFrame
        :return:  Processed comments DataFrame
        :rtype: pd.DataFrame
        """

        comments_df["Event"] = comments_df["Event"].apply(self.remove_non_caps)
        events_to_replace = {
            "LAUNCH": "LAUNCH/IGNITION",
            "BURNOUT": "BURNOUT/EJECTION_CHARGE",
            "GROUND_HIT": "GROUND_HIT/SIMULATION_END"
        }
        events_to_remove = ["IGNITION", "EJECTION_CHARGE", "SIMULATION_END"]
        comments_df["Event"] = comments_df["Event"].replace(events_to_replace)
        comments_df = comments_df[~comments_df["Event"].isin(events_to_remove)]
        return comments_df[["Time (s)", "Event"]]

    def find_event_time(self, event_name: str) -> float:
        """
        find_event_time  Finds the time when a specific event occurred.

        :param event_name:  Event name
        :type event_name: str
        :return:  Time in seconds
        :rtype: float
        """
        event_time = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Time (s)"]
        return float(event_time.iloc[0]) if not event_time.empty else None

    def find_event_mach(self, event_name: str) -> float:
        """
        find_event_mach  Finds the Mach number when a specific event occurred.

        :param event_name:  Event name
        :type event_name: str
        :return:  Mach number
        :rtype: float
        """

        event_mach = self.merged_df.loc[self.merged_df["Event"]
                                        == event_name, "Mach number ()"]
        return float(event_mach.iloc[0]) if not event_mach.empty else None

    def remove_non_caps(self, text: str) -> str:
        """
        remove_non_caps  Removes all words that are not in all caps from the given text.

        :param text:  Text to remove non-caps words from
        :type text: str
        :return:  Text with non-caps words removed
        :rtype: str
        """
        return " ".join(word for word in text.split() if word.isupper())

    def rename_or_df_columns(self):
        rename_cols = {
            "Time (s)": "time",
            "Altitude (ft)": "altitude",
            "Vertical velocity (m/s)": "vertical_velocity",
            "Vertical acceleration (m/s²)": "vertical_acceleration",
            "Total velocity (m/s)": "total_velocity",
            "Total acceleration (m/s²)": "total_acceleration",
            "Position East of launch (ft)": "position_east_of_launch",
            "Position North of launch (ft)": "position_north_of_launch",
            "Lateral distance (ft)": "lateral_distance",
            "Lateral direction (°)": "lateral_direction",
            "Lateral velocity (m/s)": "lateral_velocity",
            "Lateral acceleration (m/s²)": "lateral_acceleration",
            "Latitude (°)": "latitude",
            "Longitude (°)": "longitudinal",
            "Gravitational acceleration (m/s²)": "gravitation_acceleration",
            "Angle of attack (°)": "angle_of_attack",
            "Roll rate (r/s)": "roll_rate",
            "Pitch rate (r/s)": "pitch_rate",
            "Yaw rate (r/s)": "yaw_rate",
            "Mass (g)": "mass",
            "Motor mass (g)": "motor_mass",
            "Longitudinal moment of inertia (kg·m²)": "longitudinal_moment_of_inertia",
            "Rotational moment of inertia (kg·m²)": "rotational_moment_of_inertia",
            "CP location (mm)": "cp_location",
            "CG location (mm)": "cg_location",
            "Stability margin calibers ()": "stability_margin_calibers",
            "Mach number ()": "mach_number",
            "Reynolds number ()": "reynolds_number",
            "Thrust (N)": "thrust",
            "Drag force (N)": "drag_force",
            "Drag coefficient ()": "drag_coefficient",
            "Axial drag coefficient ()": "axial_drag_coefficient",
            "Friction drag coefficient ()": "friction_drag_coefficient",
            "Pressure drag coefficient ()": "pressure_drag_coefficient",
            "Base drag coefficient ()": "base_drag_coefficient",
            "Normal force coefficient ()": "normal_force_coefficient",
            "Pitch moment coefficient ()": "pitch_moment_coefficient",
            "Yaw moment coefficient ()": "yaw_moment_coefficient",
            "Side force coefficient ()": "side_force_coefficient",
            "Roll moment coefficient ()": "roll_moment_coefficient",
            "Roll forcing coefficient ()": "roll_forcing_coefficient",
            "Roll damping coefficient ()": "roll_damping_coefficient",
            "Pitch damping coefficient ()": "pitch_damping_coefficient",
            "Coriolis acceleration (m/s²)": "coriolis_acceleration",
            "Reference length (mm)": "reference_length",
            "Reference area (cm²)": "reference_area",
            "Vertical orientation (zenith) (°)": "vertical_orientation_zenith",
            "Lateral orientation (azimuth) (°)": "lateral_orientation_azimuth",
            "Wind velocity (m/s)": "wind_velocity",
            "Air temperature (°C)": "air_temperature",
            "Air pressure (mbar)": "air_pressure",
            "Speed of sound (m/s)": "speed_of_sound",
            "Simulation time step (s)": "simulation_time_step",
            "Computation time (s)": "computation_time",
            "Event": "event"
        }
        self.merged_df.rename(columns=rename_cols, inplace=True)

    def rename_ras_df_columns(self):
        rename_cols = {
            "Time (sec)": "time",
            "Altitude (ft)": "altitude",
            "Stage": "stage",
            "Stage Time (sec)": "stage_time",
            "Distance (ft)": "distance",
            "Mach Number": "mach_number",
            "Angle of Attack (deg)": "angle_of_attack",
            "CL":"lift_coefficient",
            "CD": "drag_coefficient",
            "Weight (lb)": "weight_imperial",
            "Thrust (lb)": "thrust_imperial",
            "Drag (lb)": "drag_force_imperial",
            "Lift (lb)": "lift_force_imperial",
            "CG (in)": "cg_location_imperial",
            "CP (in)": "cp_location_imperial",
            "Stability Margin (cal)": "stability_margin_calibers",
            "Accel (ft/sec^2)": "total_acceleration_imperial",
            "Accel-V (ft/sec^2)": "vertical_acceleration_imperial",
            "Accel-H (ft/sec^2)": "horizontal_acceleration_imperial",
            "Velocity (ft/sec)": "total_velocity_imperial",
            "Vel-V (ft/sec)": "vertical_velocity_imperial",
            "Vel-H (ft/sec)": "horizontal_velocity_imperial",
            "Pitch Attitude (deg)": "pitch_attitude",
            "Flight Path Angle (deg)": "flight_path_angle",
        }
        self.ras_df.rename(columns=rename_cols, inplace=True)

    def rename_ras_mach_cd_df_columns(self):
            rename_cols = {
                "Mach": "mach_number",
                "Alpha": "alpha",
                "Stage": "stage",
                "Stage Time (sec)": "stage_time",
                "Mach Number": "mach_number",
                "Angle of Attack (deg)": "angle_of_attack",
                "CL":"lift_coefficient",
                "CD": "drag_coefficient",
                "CD Power-Off":"drag_coefficient_power_off",
                "CD Power-On":"drag_coefficient_power_on",
                "Reynolds Number": "reynolds_number",
                "CP": "cp_location",
                "CN":"normal_force_coefficient",
                "CN Potential": "normal_force_coefficient_potential",
                "CN Viscous": "normal_force_coefficient_viscous",
                "CNalpha (0 to 4 deg) (per rad)": "normal_force_slope_angle_of_attack",
                "CP (0 to 4 deg)": "cp_location_4_deg",
                "CA Power-On":"axial_force_coefficient_power_on",
                "CA Power-Off": "axial_force_coefficient_power_off"
            }
            self.filtered_ras_df.rename(columns=rename_cols, inplace=True)

    def convert_ras_units_to_SI(self) -> None:
        """
        Converts measurement units from imperial to SI units within the `ras_df` DataFrame.

        This method updates the `ras_df` DataFrame in place, converting various imperial unit measurements
        to their corresponding SI units. The conversions include weights from pounds to grams, lengths from
        inches to millimeters and feet to meters, and velocities and accelerations from feet per unit time
        to meters per unit time. The conversion factors are defined within the method for each measurement type.

        The method assumes that the original measurements are stored in columns with '_imperial' suffixes
        and updates the corresponding columns without the suffix to reflect the converted SI unit values.

        Attributes updated:
        - weight: Converts pounds to grams.
        - thrust: Converts pounds to grams.
        - drag_force: Converts pounds to grams.
        - lift_force: Converts pounds to grams.
        - cg_location: Converts inches to millimeters.
        - cp_location: Converts inches to millimeters.
        - total_acceleration, vertical_acceleration, horizontal_acceleration: Converts feet per second squared to meters per second squared.
        - total_velocity, vertical_velocity, horizontal_velocity: Converts feet per second to meters per second.

        Note: This method modifies the `ras_df` DataFrame in place and does not return any value.
        """
        pounds_to_grams = 453.6
        inch_to_mm = 25.4
        feet_to_meter = 0.3048
        self.ras_df["weight"] = self.ras_df["weight_imperial"]*pounds_to_grams
        self.ras_df["thrust"] = self.ras_df["thrust_imperial"]*pounds_to_grams
        self.ras_df["drag_force"] = self.ras_df["drag_force_imperial"] * \
            pounds_to_grams
        self.ras_df["lift_force"] = self.ras_df["lift_force_imperial"] * \
            pounds_to_grams
        self.ras_df["cg_location"] = self.ras_df["cg_location_imperial"] * \
            inch_to_mm
        self.ras_df["cp_location"] = self.ras_df["cp_location_imperial"] * \
            inch_to_mm
        self.ras_df["total_acceleration"] = self.ras_df["total_acceleration_imperial"] * \
            feet_to_meter
        self.ras_df["vertical_acceleration"] = self.ras_df["vertical_acceleration_imperial"] * \
            feet_to_meter
        self.ras_df["horizontal_acceleration"] = self.ras_df["horizontal_acceleration_imperial"] * \
            feet_to_meter
        self.ras_df["total_velocity"] = self.ras_df["total_velocity_imperial"] * \
            feet_to_meter
        self.ras_df["vertical_velocity"] = self.ras_df["vertical_velocity_imperial"] * \
            feet_to_meter
        self.ras_df["horizontal_velocity"] = self.ras_df["horizontal_velocity_imperial"] * \
            feet_to_meter
    
    def calculate_stability_percentage(self,rocket_length:float,)->None:
        """
        Calculates the stability margin as a percentage of the rocket length for each entry in the DataFrame.

        This method computes the stability margin percentage based on the center of pressure (cp_location)
        and the center of gravity (cg_location) relative to the total length of the rocket. The stability
        margin percentage is added as a new column to the DataFrame. The calculation is performed for data
        stored in `merged_df` if `or_filepath` is not empty, and in `ras_df` if `ras_file_path` is not empty.

        The stability margin percentage is calculated as:
            ((cp_location - cg_location) / rocket_length) * 100

        This provides a measure of how aerodynamically stable the rocket is, with higher percentages indicating
        a greater margin of stability.

        Parameters:
        - rocket_length (float): The total length of the rocket in the same units as `cp_location` and `cg_location`.

        Note:
        - The method modifies `merged_df` and/or `ras_df` DataFrames in place by adding a new column
        `stability_margin_percentage` that contains the calculated values.
        - The method does not return any value.
        """
        if self.or_filepath != "":
            self.merged_df["stability_margin_percentage"] = (
                self.merged_df["cp_location"] - self.merged_df["cg_location"]) / rocket_length * 100

        # if self.ras_cd_filepath != "":
        #     self._read_RASAero_Mach_csv()
        #     self.filter_mach_from_ras_csv()

        if self.ras_file_path != "":
            self.ras_df["stability_margin_percentage"] = (
                self.ras_df["cp_location"] - self.ras_df["cg_location"]) / rocket_length * 100
            
    def round_to_increment(self,values:list[float], increment:float, direction:str):
        """
        Rounds a list of values to the nearest increment either up or down.

        This function takes a list of floating-point numbers, a specified increment by which to round, 
        and a direction ('up' or 'down') indicating whether to round towards higher or lower increments. 
        It returns the rounded value according to the direction: the highest value in the list rounded up 
        or the lowest value in the list rounded down to the nearest increment.

        Parameters:
        - values (list[float]): A list of floating-point numbers to be rounded.
        - increment (float): The increment to which the values will be rounded.
        - direction (str): The direction to round the values, either 'up' for rounding up or 'down' for rounding down.

        Returns:
        float: The rounded value according to the specified direction. For 'up', it's the maximum value in the list
        rounded up to the nearest increment. For 'down', it's the minimum value in the list rounded down to the nearest increment.

        Examples:
        >>> round_to_increment([1.5, 2.3, 3.7], 0.5, 'up')
        4.0
        >>> round_to_increment([1.5, 2.3, 3.7], 1.0, 'down')
        1.0
        """
        if direction == 'up':
            return math.ceil(max(values) / increment) * increment
        elif direction == 'down':
            return math.floor(min(values) / increment) * increment
            
        
