from dataclasses import dataclass, field
import numpy as np

@dataclass
class State:
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))           # x, y, z
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))           # vx, vy, vz
    orientation: np.ndarray = field(default_factory=lambda: np.array([1.,0.,0.,0.]))  # quaternion [w, x, y, z]
    angular_velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))   # wx, wy, wz
    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))       # ax, ay, az
    angular_acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))
