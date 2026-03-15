from vehicle import Vehicle
from scipy.spatial.transform import Rotation as R

class Logger:
    def __init__(self):
        self.timestamps = []
        self.positions = []
        self.velocities = []
        self.orientations = []

    def log(self, vehicle: Vehicle, ts):
        self.timestamps = ts
        self.positions.append(vehicle.state.position.copy())
        self.velocities.append(vehicle.state.velocity.copy())
        self.orientations.append(R.from_quat(vehicle.state.orientation.as_quat())
)
