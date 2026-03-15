import numpy as np

class Accelerometer:

    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.std = 0.02  # m/s^2 noise

    def measure(self, true_acc_world):

        # convert acceleration from world frame to body frame
        acc_body = self.vehicle.state.orientation.inv().apply(true_acc_world)

        # add noise
        noise = np.random.normal(0, self.std, 3)

        return acc_body + noise