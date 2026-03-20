import numpy as np

class Gyroscope:
    def __init__(self, vehicle):
        """
        Gyroscope sensor simulation.

        vehicle: the rocket object
        noise_std: standard deviation of noise in rad/s
        """
        self.vehicle = vehicle
        self.noise_std = .001 #rad/s

    def measure(self):

        # Add Gaussian noise
        noise = np.random.normal(0, self.noise_std, 3)
        noisy_ang_vel = self.vehicle.state.truth_ang_vel + noise

        return noisy_ang_vel