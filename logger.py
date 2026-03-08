from vehicle import Vehicle

class Logger:
    def __init__(self):
        self.positions = []
        self.velocities = []
        self.orientations = []

    def log(self, vehicle: Vehicle):
        self.positions.append(vehicle.state.position.copy())
        self.velocities.append(vehicle.state.velocity.copy())
        self.orientations.append(vehicle.state.orientation.copy())
