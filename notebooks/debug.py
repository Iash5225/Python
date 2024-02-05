from data_handler import *
# import sys
# sys.path.append("..")  # Adds the parent directory to the system pat

# from script.data_handler import *
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
sys.path.append("..")  # Adds the parent directory to the system pat
# sys.path.append("..")  # Adds the parent directory to the system pat
OR_DATA_FILE_NAME = r"C:\Users\iashb\OneDrive - The University of Western Australia\UWA\04. Aerospace\Documents\Technical Teams\Aerostructures\Software\Python\data\Design_review_10_02_2024.csv"
RAS_DATA_FILE_NAME = "RAS_Flight_Data.csv"
RAS_DATA_MACH_CD_FILE_NAME = "Ras__CD_Before_Raw.CSV"
DATA_DIRECTORY = "data"
MOTOR_NAME = "M1297"
ROCKET_LENGTH = 2860
ALTITUDE_INCREMENTS = 1000
VERTICAL_MOTION_INCREMENTS = 50
AVERAGE_THRUST = 0
MAX_MACH_RAS_OR_COMPARISON = 1

FLIGHT_PROFILE_PLOT_TITLE = f"{MOTOR_NAME} Motor - Vertical Motion vs Time"
# Columns to consider for vertical motion
VERTICAL_MOTION_COLUMNS = ['vertical_velocity', 'vertical_acceleration']
# Get the current working directory (should be 'Notebooks')
# cwd = os.getcwd()
# # Go up one level to the project directory
# project_dir = os.path.join(cwd, '..')
# # Construct the path to the CSV file in the 'data' directory
# or_csv_path = os.path.join(project_dir, DATA_DIRECTORY, OR_DATA_FILE_NAME)
# # Normalize the path (optional but recommended)
# or_csv_path = os.path.normpath(or_csv_path)

# ras_csv_path = os.path.join(project_dir, DATA_DIRECTORY, RAS_DATA_FILE_NAME)
# # Normalize the path (optional but recommended)
# ras_csv_path = os.path.normpath(ras_csv_path)

# ras_mach_cd_csv_path = os.path.join(
#     project_dir, DATA_DIRECTORY, RAS_DATA_MACH_CD_FILE_NAME)
# # Normalize the path (optional but recommended)
# ras_mach_cd_csv_path = os.path.normpath(ras_mach_cd_csv_path)

dh = DataHandler(or_filepath=OR_DATA_FILE_NAME)
dh.rename_or_df_columns()
dh.rename_ras_df_columns()
dh.convert_ras_units_to_SI()
dh.rename_ras_mach_cd_df_columns()

print(dh.merged_df)
# display(dh.ras_df)
# display(dh.filtered_ras_df)
