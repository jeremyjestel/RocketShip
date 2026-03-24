import numpy as np

class Estimator:
    def __init__(self, rocket):
        self.rocket = rocket

        # tuning parameters 
        self.k_pos = 0.05   # position GPS correction strength
        self.k_vel = 0.02   # velocity GPS correction strength

    def predict(self, imu_accel_body, dt):
        state = self.rocket.state

        # Convert acceleration from body → world frame
        accel_world = state.truth_orientation.apply(imu_accel_body)

        # Integrate acceleration → velocity → position
        state.belief_vel += accel_world * dt
        state.belief_pos += state.belief_vel * dt

    def correct(self, gps_pos, gps_vel=None):
        #Only runs when GPS updates
        state = self.rocket.state

        #  Position correction
        pos_error = gps_pos - state.belief_pos
        state.belief_pos += self.k_pos * pos_error

        #Velocity correction 
        if gps_vel is not None:
            vel_error = gps_vel - state.belief_vel
            state.belief_vel += self.k_vel * vel_error

    def step(self, sensor_data, dt):
        # 1. Predict using IMU
        imu_accel = sensor_data["imu_accel"]
        self.predict(imu_accel, dt)

        # 2. Correct using GPS (if available)
        gps_data = sensor_data["gps"]
        if gps_data is not None:
            self.correct(
                gps_data["pos"],
                gps_data.get("vel", None)
            )