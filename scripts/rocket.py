import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import math
import os


class Rocket:
    """Rocket class for plotting data from a CSV file."""

    def __init__(self, filepath: str) -> None:
        """Initialise the Rocket class for plotting data from a CSV file.

        Args:
            filepath (str):  The path to the CSV file containing the data.
        """
        # Default values for constants
        self.DATA_FILEPATH = filepath
        self.MOTOR_NAME = "Motor Name"
        self.ROCKET_LENGTH = 2000
        self.ALTITUDE_INCREMENTS = 1000
        self.VERTICAL_MOTION_INCREMENTS = 50
        self.AVERAGE_THRUST = 0
        self.OUTPUT_FOLDER_PATH = r"project\output"
        self.STABILITY_UNIT = 'cal'  # 'cal' or '%'
        self.SHOW_FULL_STABILITY_GRAPH = True  # True or False

        # Save
        self.PLOT_SAVE = False
        # Events
        self.DISPLAY_MOTOR_BURNOUT = False
        self.DISPLAY_LAUNCH = False
        self.DISPLAY_APOGEE = False
        self.DISPLAY_GROUND_HIT = False
        self.DISPLAY_LAUNCH_ROD = False

        # Load data
        self.df = self.read_csv_file()
        self.comments_df = self.extract_comments()
        self.filtered_df = self.filter_comments_from_csv()
        self.merged_df = self.merge_dataframes()
        
    def set_stability_unit(self, unit: str) -> None:
        """Set the STABILITY_UNIT variable to either 'cal' or '%'.

        Args:
            unit (str): 'cal' for calibers or '%' for percentage
        """
        if unit in ['cal', '%']:
            self.STABILITY_UNIT = unit
        else:
            print("Invalid stability unit. Please choose 'cal' or '%'.")

    def set_show_full_stability_graph(self, state: bool) -> None:
        """Set the SHOW_FULL_STABILITY_GRAPH variable to True or False.

        Args:
            state (bool): True to show full graph, False to limit to launch and burnout
        """
        self.SHOW_FULL_STABILITY_GRAPH = state
        
    def display_comments(self):
        """Prints the comments DataFrame in a well-formatted manner."""

        # Check if DataFrame exists
        if self.comments_df is None:
            print("Comments DataFrame not available.")
            return

        # Define the format for each row
        row_format ="{:<15}" * len(self.comments_df.columns)

        # Print the header
        print(row_format.format(*self.comments_df.columns))

        # Print each row
        for _, row in self.comments_df.iterrows():
            print(row_format.format(*row))

    def set_PLOT_SAVE(self, state: bool) -> None:
        """Set the PLOT_SAVE constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.PLOT_SAVE = state

    def set_DISPLAY_MOTOR_BURNOUT(self, state: bool) -> None:
        """Set the DISPLAY_MOTOR_BURNOUT constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.DISPLAY_MOTOR_BURNOUT = state

    def set_DISPLAY_LAUNCH(self, state: bool) -> None:
        """Set the DISPLAY_LAUNCH constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.DISPLAY_LAUNCH = state

    def set_DISPLAY_APOGEE(self, state: bool) -> None:
        """Set the DISPLAY_APOGEE constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.DISPLAY_APOGEE = state

    def set_DISPLAY_GROUND_HIT(self, state: bool) -> None:
        """Set the DISPLAY_GROUND_HIT constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.DISPLAY_GROUND_HIT = state

    def set_DISPLAY_LAUNCH_ROD(self, state: bool) -> None:
        """Set the DISPLAY_LAUNCH_ROD constant to True or False.

        Args:
            state (bool):  True or False
        """
        self.DISPLAY_LAUNCH_ROD = state

    def set_data_file_Path(self, filepath: str) -> None:
        """Set the DATA_FILEPATH constant to the given filepath.

        Args:
            filepath (str):  _description_
        """
        self.DATA_FILEPATH = filepath

    def set_motor_name(self, motor_name: str) -> None:
        """Set the MOTOR_NAME constant to the given motor name.

        Args:
            motor_name (str): Motor name
        """
        self.MOTOR_NAME = motor_name

    def set_rocket_length(self, length: int) -> None:
        """Set the ROCKET_LENGTH constant to the given length.

        Args:
            length (int):  Rocket length
        """
        self.ROCKET_LENGTH = length

    def set_altitude_increments(self, increments: int) -> None:
        """Set the ALTITUDE_INCREMENTS constant to the given increments.

        Args:
            increments (int):  Altitude increments
        """
        self.ALTITUDE_INCREMENTS = increments

    def set_vertical_motion_increments(self, increments: int) -> None:
        """Set the VERTICAL_MOTION_INCREMENTS constant to the given increments.

        Args:
            increments (int):  Vertical motion increments
        """
        self.VERTICAL_MOTION_INCREMENTS = increments

    def set_average_thrust(self, average_thrust: float) -> None:
        """Set the AVERAGE_THRUST constant to the given thrust.

        Args:
            average_thrust (float):  Average thrust
        """
        self.AVERAGE_THRUST = average_thrust

    def set_output_folder_path(self, path: str) -> None:
        """Set the OUTPUT_FOLDER_PATH constant to the given path.

        Args:
            path (str):  Output folder path
        """
        self.OUTPUT_FOLDER_PATH = path

    def read_csv_file(self) -> pd.DataFrame:
        """Read the CSV file and return a DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the data from the CSV file
        """

        try:
            df = pd.read_csv(self.DATA_FILEPATH, delimiter=",", skiprows=6)
            return df
        except Exception as e:
            print(f"An error occurred while reading the CSV file: {e}")
            return None

    def extract_time(self, text: str) -> float:
        """Extract the numerical value of time from a string containing 't ='

        Args:
            text (str): string containing 't ='

        Returns:
            float: numerical value of time or else None
        """
        match = re.search(r"t=([\d\.]+)", text)
        return float(match.group(1)) if match else None

    def remove_non_caps(self, text: str) -> str:
        """Removes all words that are not in all caps from the given text.

        Args:
            text (str): The string from which to remove non-uppercase words

        Returns:
            str: Modified string containing only uppercase words
        """
        return " ".join(word for word in text.split() if word.isupper())

    def extract_comments(self) -> pd.DataFrame:
        """Extracts the comments from the CSV file and returns a DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the comments from the CSV file
        """
        df = self.df
        comments_df = df[df["# Time (s)"].astype(str).str.contains("#")].copy(deep=True)
        comments_df["Time (s)"] = comments_df["# Time (s)"].apply(
            lambda x: re.search(r"t=([\d\.]+)", x).group(1)
            if re.search(r"t=([\d\.]+)", x)
            else None
        )
        comments_df["Time (s)"] = pd.to_numeric(
            comments_df["Time (s)"], errors="coerce"
        )
        comments_df["Event"] = (
            comments_df["# Time (s)"]
            .str.replace(r"occurred at t=[\d\.]+ seconds", "")
            .str.replace("#", "")
            .str.strip()
        )
        # Apply the function to the 'Event' column of your DataFrame
        comments_df["Event"] = comments_df["Event"].apply(self.remove_non_caps)

        # Rename 'LAUNCH' to 'LAUNCH/IGNITION'
        comments_df["Event"] = comments_df["Event"].replace(
            {"LAUNCH": "LAUNCH/IGNITION"}
        )
        # Rename 'BURNOUT' to 'BURNOUT/EJECTION_CHARGE'
        comments_df["Event"] = comments_df["Event"].replace(
            {"BURNOUT": "BURNOUT/EJECTION_CHARGE"}
        )
        # Rename 'GROUND_HIT' to 'GROUND_HIT/SIMULATION_END'
        comments_df["Event"] = comments_df["Event"].replace(
            {"GROUND_HIT": "GROUND_HIT/SIMULATION_END"}
        )

        # Remove the 'IGNITION' row
        comments_df = comments_df[comments_df["Event"] != "IGNITION"]
        # Remove the 'EJECTION_CHARGE' row
        comments_df = comments_df[comments_df["Event"] != "EJECTION_CHARGE"]
        # Remove the 'SIMULATION_END' row
        comments_df = comments_df[comments_df["Event"] != "SIMULATION_END"]

        return comments_df[["Time (s)", "Event"]]

    def filter_comments_from_csv(self) -> pd.DataFrame:
        """Filters out rows that contain comments from the dataframe.

        Returns:
            pd.DataFrame:  DataFrame containing the filtered data
        """
        df = self.df.copy(deep=True)
        filtered_df = df[~df["# Time (s)"].astype(str).str.contains("#")].copy(
            deep=True
        )
        filtered_df["Time (s)"] = pd.to_numeric(
            filtered_df["# Time (s)"], errors="coerce"
        )
        return filtered_df

    def merge_dataframes(self) -> pd.DataFrame:
        """Merges the filtered DataFrame with the comments DataFrame.

        Returns:
            pd.DataFrame:  DataFrame containing the merged data
        """

        merged_df = self.filtered_df.merge(self.comments_df, on="Time (s)", how="left")
        # Dropping the 'Time (s)' column from the merged DataFrame
        merged_df.drop(columns=["Time (s)"], inplace=True)

        # Ensure 'Time (s)' in filtered_df is float, if it's not already
        merged_df["# Time (s)"] = pd.to_numeric(
            merged_df["# Time (s)"], errors="coerce"
        )

        rename_dict = {"# Time (s)": "Time (s)"}
        merged_df.rename(columns=rename_dict, inplace=True)

        return merged_df

    def find_event_time(self, event_name: str) -> float:
        """Find the time when a specific event occurred.

        Args:
            event_name (str): The name of the event to find

        Returns:
            float: The time when the event occurred or None if the event was not found.
        """
        event_times = self.merged_df.loc[
            self.merged_df["Event"] == event_name, "Time (s)"
        ]
        return float(event_times.iloc[0]) if not event_times.empty else None
    
    def find_event_mach(self, event_name: str) -> float:
        """Find the time when a specific event occurred.

        Args:
            event_name (str): The name of the event to find

        Returns:
            float: The time when the event occurred or None if the event was not found.
        """
        event_times = self.merged_df.loc[
            self.merged_df["Event"] == event_name, "Mach number (​)"
        ]
        return float(event_times.iloc[0]) if not event_times.empty else None


    def plot_event_markers(self, ax):
            """Plot event markers on the provided Axes object.

            Args:
                ax (matplotlib.axes.Axes): The Axes object to plot on.
            """
            events = {
                "BURNOUT/EJECTION_CHARGE": self.DISPLAY_MOTOR_BURNOUT,
                "LAUNCH/IGNITION": self.DISPLAY_LAUNCH,
                "APOGEE": self.DISPLAY_APOGEE,
                "GROUND_HIT/SIMULATION_END": self.DISPLAY_GROUND_HIT,
                "LAUNCHROD": self.DISPLAY_LAUNCH_ROD,
            }
            for event, display in events.items():
                if display:
                    event_time = self.find_event_time(event)
                    if event_time is not None:
                        ax.axvline(x=event_time, color="r", linestyle="-", label=event)
                        ax.text(event_time, ax.get_ylim()[1], event,
                        rotation=90, verticalalignment='top', horizontalalignment='right', color='red', fontsize=8)
                        
    def plot_event_markers_mach(self, ax):
            """Plot event markers on the provided Axes object.

            Args:
                ax (matplotlib.axes.Axes): The Axes object to plot on.
            """
            events = {
                "BURNOUT/EJECTION_CHARGE": self.DISPLAY_MOTOR_BURNOUT,
                "LAUNCH/IGNITION": self.DISPLAY_LAUNCH,
                "APOGEE": self.DISPLAY_APOGEE,
                "GROUND_HIT/SIMULATION_END": self.DISPLAY_GROUND_HIT,
                "LAUNCHROD": self.DISPLAY_LAUNCH_ROD,
            }
            for event, display in events.items():
                if display:
                    event_mach = self.find_event_mach(event)
                    if event_mach is not None:
                        ax.axvline(x=event_mach, color="r", linestyle="-", label=event)
                        ax.text(event_mach, ax.get_ylim()[1], event,
                        rotation=90, verticalalignment='top', horizontalalignment='right', color='red', fontsize=8)

                    
    def plot_Flight_Profile(self) -> None:
        """Plot the Flight Profile data."""
        df = self.merged_df.copy(deep=True)
        # Calculate maximum and minimum values for plotting
        max_altitude = (
            math.ceil(df["Altitude (ft)"].max() / self.ALTITUDE_INCREMENTS)
            * self.ALTITUDE_INCREMENTS
        )
        max_vertical_motion = (
            math.ceil(
                max(
                    df["Vertical velocity (m/s)"].max(),
                    df["Vertical acceleration (m/s²)"].max(),
                )
                / self.VERTICAL_MOTION_INCREMENTS
            )
            * self.VERTICAL_MOTION_INCREMENTS
        )
        min_vertical_motion = (
            math.floor(
                min(
                    df["Vertical velocity (m/s)"].min(),
                    df["Vertical acceleration (m/s²)"].min(),
                )
                / self.VERTICAL_MOTION_INCREMENTS
            )
            * self.VERTICAL_MOTION_INCREMENTS
        )

        # Create plot
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Plot Altitude
        ax1.plot(df["Time (s)"], df["Altitude (ft)"], "k:", label="Altitude (ft)")
        ax1.set_xlabel("TIME (s)")
        ax1.set_ylabel("ALTITUDE (ft)")
        ax1.set_xlim(0, df["Time (s)"].max())
        ax1.set_ylim(0, max_altitude)
        ax1.set_yticks(range(0, max_altitude + 1, self.ALTITUDE_INCREMENTS))
        # Set x-axis ticks at regular intervals
        ax1.set_xticks(np.arange(0, df["Time (s)"].max(), 10))
        ax1.grid(True)

        # Plot Vertical velocity and acceleration
        ax2 = ax1.twinx()
        ax2.plot(
            df["Time (s)"],
            df["Vertical velocity (m/s)"],
            "k--",
            label="Vertical velocity (m/s)",
        )
        ax2.plot(
            df["Time (s)"],
            df["Vertical acceleration (m/s²)"],
            "k-",
            label="Vertical acceleration (m/s²)",
        )
        ax2.set_ylabel(
            "VERTICAL VELOCITY (m/s); VERTICAL ACCELERATION (m/s²)", labelpad=15
        )
        ax2.set_ylim(min_vertical_motion, max_vertical_motion)
        ax2.set_yticks(
            np.arange(
                min_vertical_motion,
                max_vertical_motion + 1,
                self.VERTICAL_MOTION_INCREMENTS,
            )
        )

        # Combine legends
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

        plt.title(f"{self.MOTOR_NAME} Motor - Vertical Motion vs Time")
        fig.tight_layout()

        # Plot event markers
        self.plot_event_markers(ax1)

        plt.show()

        # Save plot if required
        if self.PLOT_SAVE:
            filename = "/Flight_Profile.png"
            fig.savefig(self.OUTPUT_FOLDER_PATH + filename)
     
    def plot_Stability(self) -> None:
        """Plot Stability data."""
        df = self.merged_df.copy(deep=True)

        # Calculate stability margin percentage if needed
        if self.STABILITY_UNIT == '%':
            df["stability margin percentage"] = (
                (df["CP location (mm)"] - df["CG location (mm)"])
                / self.ROCKET_LENGTH * 100
            )

        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Select y-axis data based on STABILITY_UNIT and plot
        if self.STABILITY_UNIT == 'cal':
            ax1.plot(df["Time (s)"], df["Stability margin calibers (​)"], "k-", label="Stability(cal)")
            y_label = "STABILITY (cal)"
        else:
            ax1.plot(df["Time (s)"], df["stability margin percentage"], "k-", label="Stability(%)")
            y_label = "STABILITY (%)"

        ax1.set_xlabel("TIME (s)")
        ax1.set_ylabel(y_label)
        ax1.grid(True)

        # Plot CP and CG location on a secondary axis
        ax2 = ax1.twinx()
        ax2.plot(df["Time (s)"], df["CP location (mm)"], "r--", label="CP location (mm)")
        ax2.plot(df["Time (s)"], df["CG location (mm)"], "b--", label="CG location (mm)")
        ax2.set_ylabel("LOCATION (mm)")

        # Set x-axis limits based on SHOW_FULL_STABILITY_GRAPH
        if self.SHOW_FULL_STABILITY_GRAPH:
            ax1.set_xlim(0, df["Time (s)"].max())
        else:
            burnout_time = self.find_event_time("BURNOUT/EJECTION_CHARGE")
            ax1.set_xlim(0, burnout_time)

        # Combine legends from ax1 and ax2
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc="upper right")
        
        # Plot event markers
        self.plot_event_markers(ax1)
        
        plt.title(f"{self.MOTOR_NAME} Motor - {y_label} vs Time(s)")
        plt.show()

        # Save plot if required
        if self.PLOT_SAVE:
            filename = "/Stability.png"
            fig.savefig(self.OUTPUT_FOLDER_PATH + filename)
    
    def plot_DragCoefficient(self)->None:
        df = self.merged_df.copy(deep=True)
        fig, ax1 = plt.subplots(figsize=(12, 6))
        
        ax1.set_xlabel("Mach")
        ax1.set_ylabel("Drag Coefficient")
        ax1.grid(True)
        ax1.scatter(df["Mach number (​)"], df["Drag coefficient (​)"], color='k', s=5, label="Drag Coefficient")
       
        max_drag = math.ceil(df["Drag coefficient (​)"].max() * 10) / 10
        max_mach = math.ceil(df["Mach number (​)"].max() * 10) / 10
        
        # Find the data range for the drag coefficient
        min_drag_coefficient = df["Drag coefficient (​)"].min()
        max_drag_coefficient = df["Drag coefficient (​)"].max()

        # Add a buffer to the min and max
        buffer = (max_drag_coefficient - min_drag_coefficient) * 0.1  # 10% buffer
        min_limit = max(min_drag_coefficient - buffer, 0)  # Avoid negative lower limit
        max_limit = max_drag_coefficient + buffer
        
        max_drag_rounded = math.ceil(max_limit * 10) / 10
        min_drag_rounded = math.floor(min_limit * 10) / 10
        
        # Set the y-limits with a buffer
        # ax1.set_ylim(min_limit, max_limit)
        ax1.set_ylim(min_drag_rounded, max_drag_rounded)
        # ax1.set_ylim(0, max_drag)
        ax1.set_xlim(0,max_mach)
        
        # ax1.set_yticks(np.arange(0, max_drag+0.1, 0.05))
        
        # Plot event markers
        self.plot_event_markers_mach(ax1)
        
        plt.show()
            

    def run(self):
        # self.plot_Flight_Profile()
        # self.plot_Stability()
        self.plot_DragCoefficient()
        


def main():
    # Usage
    data_file_name = "Rocket Data.csv"

    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Go up one level to the project directory
    project_dir = os.path.join(script_dir, "..")

    # Construct the path to the CSV file
    csv_path = os.path.join(project_dir, "data", data_file_name)

    # Normalize the path (optional but recommended)
    csv_path = os.path.normpath(csv_path)
    
    profile = Rocket(csv_path)
    profile.set_motor_name("M2100")
    profile.set_rocket_length(2500)
    profile.set_altitude_increments(1000)
    # ... other settings as needed
    profile.set_DISPLAY_LAUNCH(False)
    profile.set_DISPLAY_MOTOR_BURNOUT(True)
    profile.set_DISPLAY_APOGEE(False)
    profile.set_DISPLAY_LAUNCH_ROD(False)
    profile.set_show_full_stability_graph(False)
    profile.set_stability_unit('%')
    # profile.display_comments()
    profile.run()


if __name__ == "__main__":
    main()
