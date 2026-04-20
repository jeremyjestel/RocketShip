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

    return Sim(
        rocket,
        physics,
        env,
        estimator,
        logger,
        sensors,
        params.dt,
        params.max_time,
        on_close_callback=show_input_panel,
    )


def run_simulation():
    global simulation
    if input_panel is not None and input_panel.isVisible():
        input_panel.hide()
    simulation = create_sim()


def show_input_panel():
    if input_panel is not None:
        input_panel.show()


if __name__ == '__main__':
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)
    input_panel = InputPanel(run_callback=run_simulation)
    input_panel.show()
    app.exec()

    # if sim is not None:
    #     pos_difference_vec = sim.logger.truth_positions[-1] - sim.logger.belief_positions[-1]
    #     error = np.linalg.norm(pos_difference_vec)
    #     print("Final error: ", error, " in meters")
    # else:
    #     print("Simulation was not started.")
