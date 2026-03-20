from environment import Environment
import numpy as np
from scipy.spatial.transform import Rotation as R
import config


class PhysicsEngine:
    def __init__(self, rocket):
        self.rocket = rocket
    #all newtons
    def compute_forces(self, env: Environment):
        #thrust
        thrust_body = self.rocket.engine.get_thrust()
        F_thrust = self.rocket.state.truth_orientation.apply(thrust_body)

        
        # force of gravity
        F_grav = env.get_gravity(self.rocket.state.truth_pos) * self.rocket.state.current_mass

        # force of drag adjusted for wind
        vel_wind_rel = self.rocket.state.truth_vel - env.wind
        v = np.linalg.norm(vel_wind_rel)

        if v == 0:
            F_air_resist = np.array([0,0,0])
        else:
            drag_mag = .5 * env.air_density * v ** 2 * config.drag_coefficient * config.A
            F_air_resist = -drag_mag * (vel_wind_rel / v)

        F_total = F_thrust + F_grav + F_air_resist
        return F_total

    def step_physics(self, env: Environment, dt: float):
        F_total = self.compute_forces(env)
        self.rocket.state.truth_accel = F_total / self.rocket.state.current_mass
        self.rocket.state.update_truth_state(dt, self.rocket.mass_props.burn_rate)

