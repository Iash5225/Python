import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy.interpolate import interp1d

GRAVITY = 9.81


def calc_area_cd(safety_factor: float, rocket_mass: float, air_density: float, descent_velocity: float) -> float:
    return safety_factor*(2*rocket_mass*GRAVITY) / \
        (air_density*descent_velocity**2)
