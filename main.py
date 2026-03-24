# main.py

import numpy as np
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
from rocket import Rocket
from estimator import Estimator
import config
#user adjusted params

env = Environment(
    wind=config.wind        # m/s, affects air resistance drag
)

rocket = Rocket(
    name="TestRocket",
    state = State(
        truth_pos=config.starting_pos,
        truth_vel=config.starting_vel,
        truth_ang_vel=config.starting_ang_vel,
        truth_orientation=config.starting_orientation,
        belief_pos=config.starting_pos.copy(),
        belief_vel=config.starting_vel.copy(),
        belief_ang_vel=config.starting_ang_vel.copy(),
        belief_orientation=config.starting_orientation,
        current_mass=config.init_mass,
        current_fuel_mass=config.init_mass * config.percent_fuel
    ),
    mass_props=MassProperties(
        config.init_mass,
        config.percent_fuel,
        burn_rate = config.burn_rate
    ),
    engine=Engine(
        throttle=1         # fully on
    )
)

controller = Controller(rocket)
logger = Logger(rocket)
visualizer = Visualizer(logger)
physics = PhysicsEngine(rocket)
sensors = Sensor(rocket)
estimator = Estimator(rocket) 

ts = 0.0   #timestamp

while ts < config.sim_time:
    if rocket.state.current_fuel_mass < 0:
        break

    #need to update the world, then make decisions and measurements after
    physics.step_physics(env, config.dt)

    #for now not caring bout the gps 
    sensor_data = sensors.read_sensors(ts)

    #will be kalman filter but estimates from the noisy measurement
    estimator.step(sensor_data, config.dt)

    logger.log(ts)
    ts += config.dt

pos_difference_vec = logger.truth_positions[-1] - logger.belief_positions[-1]
error = np.linalg.norm(pos_difference_vec)

print("Final error: ", error)

visualizer.plot_trajectory()
