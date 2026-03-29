import numpy as np
from scipy.spatial.transform import Rotation as R


init_mass = 549000
percent_fuel = .33
wind=np.array([0., 0., 0.])
starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 0., 0.])
starting_ang_vel = np.array([.5, 0., 0.])
starting_orientation = R.from_euler('x', 0, degrees=True)
burn_rate = 40000
max_thrust = 7600000
dt = 0.01       # timestep because sim is 100 hz
sim_time = 3   # total simulation time in seconds
drag_coefficient = .4 #ai suggested .3-.5 for rocke
A = 10  #this equation is A = pi * r ^ 2, is m ^ 2
accelerometer_std = .02

gyro_noise_std = .001 #rad/s