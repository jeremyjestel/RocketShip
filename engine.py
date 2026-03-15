from dataclasses import dataclass, field
import numpy as np

@dataclass

class Engine:
    max_thrust = 7600000 #example number for now in N
    throttle: float = 0.0   # 0 to 1
    fuel_mass: float = 0.0
    thrust_vec = np.array([0,0,max_thrust])  #stored in body frame of reference, converted to world frame 

    def get_thrust(self):
        # Returns current thrust vector
        return self.thrust_vec * self.throttle
