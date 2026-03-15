from dataclasses import dataclass, field
import numpy as np
from scipy.spatial.transform import Rotation as R

@dataclass
class State:
    #these are in world coordinates
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    #The orientation encodes the rotation needed to get from body → world
    orientation: R = field(default_factory=R.identity)   # scipy rotaion, updated with angular velocity
    #this is in body frame reference
    angular_velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    angular_acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))#leaving zeroes for now, hardcoded and doesn't change yet

    def update_state(self, acc, dt):
        self.acceleration = acc
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

