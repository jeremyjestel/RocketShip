from vehicle import Rocket
from environment import Environment
import numpy as np
from scipy.spatial.transform import Rotation as R


class PhysicsEngine:
    #all newtons
    def compute_forces(self, vehicle: Rocket, env: Environment):
        #thrust
        thrust_body = vehicle.engine.get_thrust()
        F_thrust = vehicle.state.true_orientation.apply(thrust_body)

        
        # force of gravity
        F_grav = env.get_gravity(vehicle.state.true_pos) * vehicle.state.current_mass

        # force of drag adjusted for wind
        drag_coefficient = .4 #ai suggested .3-.5 for rocket
        vel_wind_rel = vehicle.state.true_vel - env.wind
        v = np.linalg.norm(vel_wind_rel)
        A = 10  #this equation is A = pi * r ^ 2, is m ^ 2

        if v == 0:
            F_air_resist = np.array([0,0,0])
        else:
            drag_mag = .5 * env.air_density * v ** 2 * drag_coefficient * A
            F_air_resist = -drag_mag * (vel_wind_rel / v)

        total_force = F_thrust + F_grav + F_air_resist
        return total_force

    def step_linear(self, vehicle: Rocket, env: Environment, dt: float):
        F_total = self.compute_forces(vehicle, env)
        true_accel = F_total / vehicle.state.current_mass
        vehicle.state.update_state(true_accel, dt, vehicle.mass_props.burn_rate)

    def step_rotational(self, vehicle: Rocket, dt: float):
        vehicle.state.true_ang_vel += vehicle.state.true_ang_accel * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(vehicle.state.true_ang_vel * dt)
        vehicle.state.true_orientation = delta_orientation * vehicle.state.true_orientation
