# main.py

import numpy as np
from guts.state import State
from guts.engine import Engine
from guts.environment import Environment
from guts.physics import PhysicsEngine
from guts.controller import Controller
from UI.logger import Logger
from UI.visualizer import Visualizer
from scipy.spatial.transform import Rotation as R
from sensors.sense import Sensor
from guts.rocket import Rocket
from sensors.estimator import Basic_Estimator
import params
from PyQt6.QtWidgets import QApplication
from guts.sim import Sim
from UI.input_panel import InputPanel

simulation = None
input_panel = None


def create_sim():
    env = Environment(wind=params.wind)

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
        engine=Engine(throttle=params.throttle, burn_rate=params.burn_rate),
    )

    Controller(rocket)
    logger = Logger(rocket)
    Visualizer(logger)
    physics = PhysicsEngine(rocket)
    sensors = Sensor(rocket)
    estimator = Basic_Estimator(rocket)

    return {
        "rocket": rocket,
        "physics": physics,
        "env": env,
        "estimator": estimator,
        "logger": logger,
        "sensors": sensors,
        "dt": params.dt,
        "max_time": params.max_time,
    }


def run_simulation():
    global simulation
    sim_args = create_sim()
    if simulation is None:
        simulation = Sim(**sim_args, session_end_callback=show_input_panel)
        return
    simulation.reset_session(**sim_args)


def show_input_panel():
    if input_panel is not None:
        input_panel.show()
        input_panel.raise_()
        input_panel.activateWindow()


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    input_panel = InputPanel(run_callback=run_simulation)
    input_panel.show()
    app.exec()

    # if sim is not None:
    #     pos_difference_vec = sim.logger.truth_positions[-1] - sim.logger.belief_positions[-1]
    #     error = np.linalg.norm(pos_difference_vec)
    #     print("Final error: ", error, " in meters")
    # else:
    #     print("Simulation was not started.")
