from dataclasses import dataclass, field
import numpy as np
import params
@dataclass
class Engine:
    throttle: float = params.throttle   # 0 to 1
    thrust_vec = np.array([0,0,params.max_thrust])  #stored in body frame of reference, converted to world frame 
    burn_rate = 0
    max_thrust = 0

    def __init__(self, throttle, burn_rate, max_thrust):
        self.throttle = throttle
        self.burn_rate = burn_rate
        self.max_thrust = max_thrust

    def get_thrust(self):
          return np.array([0, 0, self.max_thrust]) * self.throttle