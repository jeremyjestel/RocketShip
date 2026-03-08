from vehicle import Vehicle

class Sensor:
    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def read(self):
        # Returns perfect measurements for now
        return self.vehicle.state
