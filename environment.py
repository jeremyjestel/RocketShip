from dataclasses import dataclass, field
import numpy as np

@dataclass
class Environment:
    gravity: np.ndarray = field(default_factory=lambda: np.array([0., 0., -9.81]))
    air_density: float = 1.225  # kg/m^3 at sea level
    wind: np.ndarray = field(default_factory=lambda: np.zeros(3))

    def get_gravity(self, position=None):
        # could vary with altitude later
        return self.gravity
