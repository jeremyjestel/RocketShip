from vehicle import Rocket
from scipy.spatial.transform import Rotation as R
import numpy as np

class Logger:
    def __init__(self):
        self.timestamps = []
        self.positions = []
        self.velocities = []
        self.accelerations = []
        self.orientations = []

    def log(self, vehicle: Rocket, ts):
        self.timestamps.append(np.round(ts, decimals=1))
        self.positions.append(vehicle.state.true_pos.copy())
        self.velocities.append(vehicle.state.true_vel.copy())
        self.accelerations.append(vehicle.state.true_accel.copy())
        self.orientations.append(R.from_quat(vehicle.state.true_orientation.as_quat()))
    
    def print_log(self):
        for i in range(len(self.timestamps)):
            print("Timestamp: ", self.timestamps[i], ", Position Vector: ", self.positions[i], ", Velocity Vector: ", self.velocities[i], ", Acceleration Vector: ", self.accelerations[i])
