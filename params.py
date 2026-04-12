import numpy as np
from scipy.spatial.transform import Rotation as R


init_mass = 549000
percent_fuel = .33
#thjese have to be floats
wind=np.array([0., 0., 0.])
starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 0., 0.])
starting_ang_vel = np.array([0.5, 0, 0])

# normalize (avoid zero division)
if np.linalg.norm(starting_vel) < 1e-8:
    starting_orientation = R.identity()
else:
    v_dir = starting_vel / np.linalg.norm(starting_vel)
    body_forward = np.array([0, 0, 1])  # rocket body axis
    # align_vectors(a, b) returns a rotation that maps b -> a.
    # We want body_forward -> velocity direction, so pass (v_dir, body_forward).
    alignment_result = R.align_vectors([v_dir], [body_forward])
    starting_orientation = alignment_result[0]

burn_rate = 40000
max_thrust = 76000000
dt = 1       # timestep because sim is 100 hz
max_time = 100   # total simulation time in seconds
drag_coefficient = .4 #ai suggested .3-.5 for rocke
A = 10  #this equation is A = pi * r ^ 2, is m ^ 2
accelerometer_std = .02
gyro_noise_std = .001 #rad/s
quadrants = 90
throttle = .1

# Control sensitivity parameter
control_sensitivity = 1  # radians per second for attitude control
throttle_sensitivity = 0.01  # throttle change per timestep for arrow keys

