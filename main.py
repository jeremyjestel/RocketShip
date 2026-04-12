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
from PyQt6.QtWidgets import QApplication
from sim import Sim
from input_panel import InputPanel

sim = None


def create_sim():
    env = Environment(
        wind=params.wind        # m/s, affects air resistance drag
    )

    rocket = Rocket(
        name="TestRocket",
        state=State(
            truth_pos=params.starting_pos,
            truth_vel=params.starting_vel,
            truth_ang_vel=params.starting_ang_vel,
            truth_orientation=params.starting_orientation,
            belief_pos=params.starting_pos.copy(),
            belief_vel=params.starting_vel.copy(),
            belief_ang_vel=params.starting_ang_vel.copy(),
            belief_orientation=params.starting_orientation,
            current_mass=params.init_mass,
            current_fuel_mass=params.init_mass * params.percent_fuel,
        ),
        mass_props=MassProperties(
            params.init_mass,
            params.percent_fuel,
            burn_rate=params.burn_rate,
        ),
        engine=Engine(
            throttle=params.throttle,
        ),
    )

    Controller(rocket)
    logger = Logger(rocket)
    Visualizer(logger)
    physics = PhysicsEngine(rocket)
    sensors = Sensor(rocket)
    estimator = Basic_Estimator(rocket)

    return Sim(rocket, physics, env, estimator, logger, sensors, params.dt, params.max_time)


def run_simulation():
    global sim
    sim = create_sim()


if __name__ == '__main__':
    app = QApplication([])
    panel = InputPanel(run_callback=run_simulation)
    panel.show()
    app.exec()

    if sim is not None:
        pos_difference_vec = sim.logger.truth_positions[-1] - sim.logger.belief_positions[-1]
        error = np.linalg.norm(pos_difference_vec)
        print("Final error: ", error, " in meters")
    else:
        print("Simulation was not started.")
