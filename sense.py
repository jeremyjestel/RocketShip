from vehicle import Vehicle
import numpy as np
from GPS import GPS


class Sensor:
    def __init__(self, vehicle: Vehicle):
        self.vehicle = vehicle
        self.GPS = GPS(vehicle)
        self.std_hor = 3.0
        self.std_vert = 7.0
        self.std_vel = .2


    def read_sensors(self):
        measured_GPS = self.GPS.measure(self.vehicle)
        
        return self.vehicle.state
