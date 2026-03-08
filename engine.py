from dataclasses import dataclass, field
import numpy as np

@dataclass

class Engine:
    max_thrust: float = 0.0
    throttle: float = 0.0                     # 0 to 1
    thrust_vector: np.ndarray = field(default_factory=lambda: np.zeros(3))  # in body frame
    fuel_mass: float = 0.0

    def get_thrust(self):
        # Returns current thrust vector
        return self.thrust_vector * self.throttle
