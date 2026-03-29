from dataclasses import dataclass, field
import numpy as np
import params
@dataclass
class Engine:
    throttle: float = 0.0   # 0 to 1
    fuel_mass: float = 0.0
    thrust_vec = np.array([0,0,params.max_thrust])  #stored in body frame of reference, converted to world frame 

    def get_thrust(self):
        # Returns current thrust vector
        return self.thrust_vec * self.throttle
