from dataclasses import dataclass, field
import numpy as np

@dataclass
class Rocket():
    name: str = ""

    # Position 
    position: np.ndarray = field(default_factory=lambda: np.zeros(3))  # [x, y, z]

    # Linear velocity 
    velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))  # [vx, vy, vz]

    # Orientation 
    orientation: np.ndarray = field(default_factory=lambda: np.array([1.0,0.0,0.0,0.0]))
    
    # Angular velocity 
    angular_velocity: np.ndarray = field(default_factory=lambda: np.zeros(3))  # [wx, wy, wz]

    # Thrust
    thrust_body: np.ndarray = field(default_factory=lambda: np.zeros(3)) 
    throttle: float = 0.0  # 0–1 scalar multiplier

    # Mass properties
    mass: float = 1000.0  # kg
    center_of_mass: np.ndarray = field(default_factory=lambda: np.zeros(3))  # relative to body frame
    inertia: np.ndarray = field(default_factory=lambda: np.eye(3))  

    # Environment
    gravity_vector: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, -9.81]))  # m/s²

    acceleration: np.ndarray = field(default_factory=lambda: np.zeros(3))