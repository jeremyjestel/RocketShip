from dataclasses import dataclass, field
import numpy as np
from scipy.spatial.transform import Rotation as R

@dataclass
class State:
    #these are in world coordinates
    true_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    true_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    true_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az

    #this is in body frame reference
    true_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    true_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet

    #The orientation encodes the rotation needed to get from body → world
    true_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity

    #the state the rocket believes it is in
    belief_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    belief_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    belief_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    belief_ang_vel: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    belief_ang_accel: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet
    belief_orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity

    current_mass: float = 1000
    current_fuel_mass: float = 1000

    def update_state(self, accel, dt, burn_rate):
        self.true_accel = accel
        self.true_vel += self.true_accel * dt
        self.true_pos += self.true_vel * dt

        self.current_mass -= burn_rate * dt
        self.current_fuel_mass -= burn_rate * dt

