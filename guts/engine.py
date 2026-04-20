from dataclasses import dataclass, field
import numpy as np
import params
@dataclass
class Engine:
    throttle: float = params.throttle   # 0 to 1
    thrust_vec = np.array([0,0,params.max_thrust])  #stored in body frame of reference, converted to world frame 
    burn_rate = 0

    def __init__(self, throttle, burn_rate):
        self.throttle = throttle
        self.burn_rate = burn_rate

    def get_thrust(self):
        # Returns current thrust vector
        return self.thrust_vec * self.throttle
