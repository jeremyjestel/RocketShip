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
from estimator import Basic_Estimator
import params
from vispy import scene
from vispy.app import Timer, run
from vispy.scene.visuals import Line
from update import update_sim
from step import step_sim
from init_vis import init_vis
from sim import Sim
#user adjusted params

env = Environment(
    wind=params.wind        # m/s, affects air resistance drag
)

rocket = Rocket(
    name="TestRocket",
    state = State(
        truth_pos=params.starting_pos,
        truth_vel=params.starting_vel,
        truth_ang_vel=params.starting_ang_vel,
        truth_orientation=params.starting_orientation,
        belief_pos=params.starting_pos.copy(),
        belief_vel=params.starting_vel.copy(),
        belief_ang_vel=params.starting_ang_vel.copy(),
        belief_orientation=params.starting_orientation,
        current_mass=params.init_mass,
        current_fuel_mass=params.init_mass * params.percent_fuel
    ),
    mass_props=MassProperties(
        params.init_mass,
        params.percent_fuel,
        burn_rate = params.burn_rate
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
estimator = Basic_Estimator(rocket) 

dt = 0.1
max_time = 10.0  # seconds

sim = Sim(rocket, physics, env, estimator, logger, sensors, dt, max_time)

if __name__ == '__main__':
    run()

pos_difference_vec = logger.truth_positions[-1] - logger.belief_positions[-1]
error = np.linalg.norm(pos_difference_vec)

print("Final error: ", error, " in meters")

# visualizer.plots_window()
