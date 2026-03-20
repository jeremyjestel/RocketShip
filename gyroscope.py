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
        self.angular_velocity = np.zeros(3)  # last measurement

    def measure(self):
        """
        Returns angular velocity in the body frame with noise.
        """
        #stored in world frame just adjusts for the fact orientation make coordinates odd
        # Get truth angular velocity in world frame
        omega_world = self.vehicle.state.truth_ang_vel  # [wx, wy, wz]

        # Convert to body frame
        omega_body = self.vehicle.state.truth_orientation.inv().apply(omega_world)

        # Add Gaussian noise
        noise = np.random.normal(0, self.noise_std, 3)
        self.angular_velocity = omega_body + noise

        return self.angular_velocity