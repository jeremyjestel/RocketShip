from vehicle import Vehicle
from environment import Environment
import numpy as np
from scipy.spatial.transform import Rotation as R


class PhysicsEngine:
    #all newtons
    def compute_forces(self, vehicle: Vehicle, env: Environment):
        #thrust
        thrust_body = vehicle.engine.get_thrust()
        F_thrust = vehicle.state.orientation.apply(thrust_body)

        
        # force of gravity
        F_grav = env.get_gravity(vehicle.state.position) * vehicle.mass_props.mass

        # force of drag adjusted for wind
        drag_coefficient = .4 #ai suggested .3-.5 for rocket
        vel_wind_rel = vehicle.state.velocity - env.wind
        v = np.linalg.norm(vel_wind_rel)
        A = 10  #this equation is A = pi * r ^ 2, is m ^ 2

        if v == 0:
            F_air_resist = np.array([0,0,0])
        else:
            drag_mag = .5 * env.air_density * v ** 2 * drag_coefficient * A
            F_air_resist = -drag_mag * (vel_wind_rel / v)

        total_force = F_thrust + F_grav + F_air_resist
        return total_force

    def step_linear(self, vehicle: Vehicle, env: Environment, dt: float):
        F_total = self.compute_forces(vehicle, env)
        acc = F_total / vehicle.mass_props.mass
        vehicle.state.update_state(acc, dt)

    def step_rotational(self, vehicle: Vehicle, dt: float):
        vehicle.state.angular_velocity += vehicle.state.angular_acceleration * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(vehicle.state.angular_velocity * dt)
        vehicle.state.orientation = delta_orientation * vehicle.state.orientation
