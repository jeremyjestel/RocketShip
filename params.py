import numpy as np
from scipy.spatial.transform import Rotation as R

percent_fuel = .33
#thjese have to be floats
wind=np.array([0., 0., 0.])
starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 0., 0.])
starting_ang_vel = np.array([0, 0, 0])

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

burn_rate = 5
max_thrust = 20000
dt = .01       # timestep because sim is 100 hz
max_time = 100   # total simulation time in seconds
drag_coefficient = .4 #ai suggested .3-.5 for rocke
A = 10  #this equation is A = pi * r ^ 2, is m ^ 2
accelerometer_std = .02
gyro_noise_std = .001 #rad/s
quadrants = 90
throttle = .5
grid_size = 1000  # size of the visualization grid in meters
line_spacing = 200

# Control sensitivity parameter
control_sensitivity = 1  # radians per second for attitude control
throttle_sensitivity = 0.01  # throttle change per timestep for arrow keys

#doing vertical launch so distance reference will be butt of rocket
#position is body frame coords
stage_configs = [
    {
        "name": "engine",
        "base_z": 0.0,
        "height": 2.0,
        "radius": 0.5,
        "mass": 250.0,
        "fuel_capacity": 0.0,
        "normal_force_coeff": 0.3,
        "aero_center_frac": 0.5,
    },
    {
        "name": "fuel tank",
        "base_z": 2.0,
        "height": 2.0,
        "radius": 0.3,
        "mass": 900.0,
        "fuel_capacity": None,
        "normal_force_coeff": 0.2,
        "aero_center_frac": 0.5,
    },
    {
        "name": "payload",
        "base_z": 4.0,
        "height": 2.0,
        "radius": 0.1,
        "mass": 120.0,
        "fuel_capacity": 0.0,
        "normal_force_coeff": 1.0,
        "aero_center_frac": 0.5,
    },
]

init_mass = sum(stage["mass"] for stage in stage_configs)
total_height = max(stage["base_z"] + stage["height"] for stage in stage_configs)


