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

# #this will be the inertial calculation with multi stage
# stage_1 = {
#     "name": "engine section",
#     "mass": 250,
#     "position": [0, 0, 0.8],
#     "inertia": [120, 120, 25],
# }

# stage_2 = {
#     "name": "fuel tank",
#     "mass": 900,
#     "position": [0, 0, 6.0],
#     "inertia": [3200, 3200, 180],
# }

# stage_3 = {
#     "name": "nose / payload",
#     "mass": 120,
#     "position": [0, 0, 11.0],
#     "inertia": [260, 260, 35],
# }

# stages = [stage_1, stage_2, stage_3]

# masses = [stages["mass"] for stages in stages]
# positions = [stages["position"] for stages in stages]

# init_mass = sum(masses)

# center_of_mass = sum(
#     stage["mass"] * np.array(stage["position"], dtype=float)
#     for stage in stages
# ) / init_mass


# total_height = sum(stages["position"][2] for stages in stages)

#going to start as cylinder for calculation of overall 

#rocket size in meters
init_mass = 1000 #kg
radius = .3
h = 6
engine_pos = np.array([0, 0, -h/2])

COM = np.array([0,0,0])
CP = np.array([0,0,-.2 *h]) #move center of pressure into the physics.py with velocity adjustment


Ixx = (1/12) * init_mass * (3 * radius ** 2 + h **2)
Iyy = (1/12) * init_mass * (3 * radius ** 2 + h **2)
Izz = .5 * init_mass * radius ** 2

inertia_vec = np.diag(np.array([Ixx, Iyy, Izz]))


