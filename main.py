# main.py

import numpy as np
from vehicle import Rocket
from state import State
from mass_properties import MassProperties
from engine import Engine
from environment import Environment
from physics import PhysicsEngine
from controller import Controller
from logger import Logger
from visualizer import Visualizer
from scipy.spatial.transform import Rotation as R
from sense import Sensor

init_mass = 549000
percent_fuel = .33

starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 0., 0.])
starting_orientation = R.from_euler('x', 0, degrees=True)

env = Environment(
    wind=np.array([0., 0., 0.])         # m/s, affects air resistance drag
)

rocket = Rocket(
    name="TestRocket",
    state = State(
        true_pos=starting_pos,
        true_vel=starting_vel,
        true_orientation=starting_orientation,
        current_mass=init_mass
    ),
    mass_props=MassProperties(
        init_mass,
        percent_fuel,
        burn_rate = 5.0
    ),
    engine=Engine(
        throttle=1         # fully on
    )
)

controller = Controller(rocket)
logger = Logger()
visualizer = Visualizer(logger)
physics = PhysicsEngine()
sensors = Sensor(rocket)

dt = 0.01       # timestep because sim is 100 hz
ts = 0.0   #timestamp
sim_time = .1   # total simulation time in seconds


while ts < sim_time:
    #need to update the world, then make decisions and measurements after
    physics.step_linear(rocket, env, dt)
    physics.step_rotational(rocket, dt)

    sensor_data = sensors.read_sensors()



    logger.log(rocket, ts)
    ts += dt

logger.print_log()
visualizer.plot_trajectory()