import numpy as np
import config

class Gyroscope:
    def __init__(self, vehicle):
        """
        Gyroscope sensor simulation.

        vehicle: the rocket object
        noise_std: standard deviation of noise in rad/s
        """
        self.vehicle = vehicle

    def measure(self):

        # Add Gaussian noise
        noise = np.random.normal(0, config.gyro_noise_std, 3)
        noisy_ang_vel = self.vehicle.state.truth_ang_vel + noise

        return noisy_ang_vel