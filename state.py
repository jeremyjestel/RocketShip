from dataclasses import dataclass, field
import numpy as np
from scipy.spatial.transform import Rotation as R

@dataclass
class State:
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    orientation: R = field(default_factory=R.identity)   # quaternion [w, x, y, z]
    angular_velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    angular_acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def update_state(self, dt):
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt

