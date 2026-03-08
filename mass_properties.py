from dataclasses import dataclass, field
import numpy as np
@dataclass
class MassProperties:
    mass: float = 1000.0                                      # kg
    center_of_mass: np.ndarray = field(default_factory=lambda: np.zeros(3))
    inertia_tensor: np.ndarray = field(default_factory=lambda: np.eye(3))  # 3x3 matrix
