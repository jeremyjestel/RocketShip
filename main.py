# main.py

import numpy as np
from vehicle import Vehicle
from state import State
from mass_properties import MassProperties
from engine import Engine
from environment import Environment
from physics_engine import PhysicsEngine
from controller import Controller
from logger import Logger
from visualizer import Visualizer


env = Environment(
    gravity=np.array([0., 0., -9.81]),  # m/s^2
    air_density=1.225,                  # kg/m^3
    wind=np.array([0., 0., 0.])         # m/s
)


rocket = Vehicle(
    name="TestRocket",
    state=State(
        position=np.array([0., 0., 0.]),
        velocity=np.array([0., 0., 0.])
    ),
    mass_props=MassProperties(
        mass=1000.0,
        center_of_mass=np.array([0., 0., 0.])
    ),
    engine=Engine(
        max_thrust=3000.0,    # Newtons
        throttle=1.0         # fully on
    )
)

controller = Controller(rocket)
logger = Logger()
visualizer = Visualizer(logger)
physics = PhysicsEngine()

dt = 0.01        # timestep
ts = 0.0   #timestamp
sim_time = 5.0   # total simulation time in seconds


while ts < sim_time:

    physics.step_linear(rocket, env, dt)
    logger.log(rocket, ts)
    ts += dt


visualizer.plot_trajectory()