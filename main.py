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

#user adjusted params
init_mass = 549000
percent_fuel = .33
starting_pos = np.array([0., 0., 0.])
starting_vel = np.array([0., 0., 0.])
starting_ang_vel = np.array([0., 0., 0.])
starting_orientation = R.from_euler('x', 0, degrees=True)

env = Environment(
    wind=np.array([0., 0., 0.])         # m/s, affects air resistance drag
)

rocket = Rocket(
    name="TestRocket",
    state = State(
        truth_pos=starting_pos,
        truth_vel=starting_vel,
        truth_ang_vel=starting_ang_vel,
        truth_orientation=starting_orientation,
        belief_pos=starting_pos.copy(),
        belief_vel=starting_vel.copy(),
        belief_ang_vel=starting_ang_vel.copy(),
        belief_orientation=starting_orientation,
        current_mass=init_mass,
        current_fuel_mass=init_mass * percent_fuel
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
logger = Logger(rocket)
visualizer = Visualizer(logger)
physics = PhysicsEngine(rocket)
sensors = Sensor(rocket)


ts = 0.0   #timestamp
dt = 0.01       # timestep because sim is 100 hz
sim_time = 3   # total simulation time in seconds


while ts < sim_time:
    if rocket.state.current_fuel_mass < 0:
        break

    #need to update the world, then make decisions and measurements after
    physics.step_physics(env, dt)

    #for now not caring bout the gps 
    sensors.read_sensors(ts, dt, env)

    logger.log(ts)
    ts += dt

pos_difference_vec = logger.truth_positions[-1] - logger.belief_positions[-1]
error = np.linalg.norm(pos_difference_vec)

print("Final error: ", error)

visualizer.plot_trajectory()
