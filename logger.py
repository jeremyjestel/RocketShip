from vehicle import Vehicle
from scipy.spatial.transform import Rotation as R
import numpy as np

class Logger:
    def __init__(self):
        self.timestamps = []
        self.positions = []
        self.velocities = []
        self.accelerations = []
        self.orientations = []

    def log(self, vehicle: Vehicle, ts):
        self.timestamps.append(np.round(ts, decimals=1))
        self.positions.append(vehicle.state.position.copy())
        self.velocities.append(vehicle.state.velocity.copy())
        self.accelerations.append(vehicle.state.acceleration.copy())
        self.orientations.append(R.from_quat(vehicle.state.orientation.as_quat()))
    
    def print_log(self):
        for i in range(len(self.timestamps)):
            print("Timestamp: ", self.timestamps[i], ", Position Vector: ", self.positions[i], ", Velocity Vector: ", self.velocities[i], ", Acceleration Vector: ", self.accelerations[i])
