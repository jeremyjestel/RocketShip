from guts.Environment import Environment
import numpy as np
from scipy.spatial.transform import Rotation as R
import params


class PhysicsEngine:
    def __init__(self, rocket):
        self.rocket = rocket
    #all newtons
    def compute_forces(self, env: Environment):
        #thrust
        thrust_body = self.rocket.engine.get_thrust()
        r_thrust = self.rocket.state.engine_pos - self.rocket.state.COM
        tau_thrust_body = np.cross(r_thrust, thrust_body)
        # tau_thrust = self.rocket.state.truth_orientation.apply(tau_thrust_body)
        F_thrust = self.rocket.state.truth_orientation.apply(thrust_body)
    
        
        # force of gravity
        F_grav = env.get_gravity(self.rocket.state.truth_pos) * self.rocket.state.current_mass
        


        # force of drag adjusted for wind
        vel_wind_rel = self.rocket.state.truth_vel - env.wind
        v = np.linalg.norm(vel_wind_rel)


        if v == 0:
            F_drag = np.array([0,0,0])
        else:
            drag_mag = .5 * env.air_density * v ** 2 * params.drag_coefficient * params.A
            F_drag = -drag_mag * (vel_wind_rel / v)

        F_drag_body = self.rocket.state.truth_orientation.inv().apply(F_drag)

        r_drag_body = self.rocket.state.CP - self.rocket.state.COM

        tau_drag_body = np.cross(r_drag_body, F_drag_body)
        # tau_drag = self.rocket.state.truth_orientation.apply(tau_drag_body)

        tau_body = tau_thrust_body + tau_drag_body #torque of gravity is zero becaus applied to COM
        F_total = F_thrust + F_grav + F_drag
        return F_total, tau_body

    def step_physics(self, env: Environment, dt: float):
        F_total, tau_body = self.compute_forces(env)


        I = self.rocket.state.I_sum
        omega = self.rocket.state.truth_ang_vel
        self.rocket.state.truth_ang_accel = np.linalg.inv(I) @ (tau_body - np.cross(omega, I @ omega))

        self.rocket.state.truth_accel = F_total / self.rocket.state.current_mass
        
        self.rocket.state.update_truth_state(dt, self.rocket.engine.burn_rate, self.rocket.engine.throttle)

