import numpy as np

class Accelerometer:

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.std = 0.02  # m/s^2 noise

    def measure(self):

        # convert acceleration from world frame to body frame
        accel_body = self.vehicle.state.true_orientation.inv().apply(self.vehicle.state.true_accel)

        # add noise
        noise = np.random.normal(0, self.std, 3)

        return accel_body + noise