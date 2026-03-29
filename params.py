import numpy as np
from scipy.spatial.transform import Rotation as R


init_mass = 549000
percent_fuel = .33
wind=np.array([0., 0., 0.])
starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 10., 5.])
starting_ang_vel = np.array([0, 0, 0.])
starting_orientation = R.from_euler('x', 0, degrees=True)
burn_rate = 40000
max_thrust = 7600000
dt = 0.01       # timestep because sim is 100 hz
max_time = 20   # total simulation time in seconds
drag_coefficient = .4 #ai suggested .3-.5 for rocke
A = 10  #this equation is A = pi * r ^ 2, is m ^ 2
accelerometer_std = .02
gyro_noise_std = .001 #rad/s


# ============ TEST CASE 4: ROTATION + TRANSLATION (COMPLEX) ============
# Rotate around Y while moving in +X - mismatch would be obvious
init_mass = 1000
percent_fuel = 0.33
wind = np.array([0., 0., 0.])
starting_pos = np.array([50., 50., 50.])
starting_vel = np.array([0., 5., 10.])  # moving in +X
starting_ang_vel = np.array([0., 0, 0.])  # pitching (Y rotation)
starting_orientation = R.from_euler('xyz', [0, 0, 0], degrees=True)
burn_rate = 0  # NO FUEL BURN - test frames only
max_thrust = 0  # NO THRUST - test frames only

dt = 0.01       # timestep
max_time = 1    # short sim to visualize
drag_coefficient = 0  # NO DRAG - pure kinematics
A = 10
accelerometer_std = 0  # NO NOISE
gyro_noise_std = 0