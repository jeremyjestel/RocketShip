from dataclasses import dataclass, field
import numpy as np
from scipy.spatial.transform import Rotation as R

@dataclass
class State:
    #these are in world coordinates
    truth_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    truth_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    truth_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az

    #this is in body frame reference
    truth_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    truth_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet

    #The orientation encodes the rotation needed to get from body → world
    truth_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity

    #the state the rocket believes it is in
    belief_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    belief_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    belief_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    belief_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    belief_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet
    belief_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity

    current_mass: float = 1000
    current_fuel_mass: float = 1000

    def update_truth_state(self, dt, burn_rate):
        self.truth_vel += self.truth_accel * dt
        self.truth_pos += self.truth_vel * dt

        self.truth_ang_vel += self.truth_ang_accel * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(self.truth_ang_vel * dt)
        self.truth_orientation = self.truth_orientation * delta_orientation 

        self.current_mass -= burn_rate * dt
        self.current_fuel_mass -= burn_rate * dt

    def update_belief_state(self, dt):
        self.belief_vel += self.belief_accel * dt
        self.belief_pos += self.belief_vel * dt

        self.belief_ang_vel += self.belief_ang_accel * dt  # rad/s
        
        # update orientation
        delta_orientation = R.from_rotvec(self.belief_ang_vel * dt)
        self.belief_orientation = delta_orientation * self.belief_orientation
