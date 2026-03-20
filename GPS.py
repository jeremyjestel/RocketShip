import numpy as np

class GPS:
    def __init__(self, vehicle):        
        self.update_rate = 5 #hz hardcoded for now
        self.vehicle = vehicle
        self.update_interval = 1.0 / self.update_rate  # seconds
        self.last_update_time = 0.0

        # Position noise (meters)
        self.horiz_std = 3.0  # horizontal accuracy
        self.vert_std = 7.0   # vertical accuracy

        # Velocity noise (m/s)
        self.vel_std = 0.2

        # Last measurement storage
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)

    def measure(self, time):
        if time - self.last_update_time >= self.update_interval or time == 0: #because gps refresh lower hz then sim timestep
            # Position measurement
            pos_noise = np.array([
                np.random.normal(0, self.horiz_std),
                np.random.normal(0, self.horiz_std),
                np.random.normal(0, self.vert_std)
            ])
            self.position = self.vehicle.state.truth_pos + pos_noise

            # Velocity measurement
            vel_noise = np.random.normal(0, self.vel_std, 3)
            self.velocity = self.vehicle.state.truth_vel + vel_noise

            # Update timestamp
            self.last_update_time = time

        return self.position, self.velocity