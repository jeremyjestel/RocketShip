from dataclasses import dataclass, field
import numpy as np
@dataclass
class MassProperties:
    mass: float = 1000.0                  
    center_of_mass: np.ndarray = field(default_factory=lambda: np.zeros(3))
