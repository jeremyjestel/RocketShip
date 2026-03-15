from vehicle import Rocket
import numpy as np
from GPS import GPS
from gyroscope import Gyroscope
from accelerometer import Accelerometer

class Sensor:
    def __init__(self, vehicle: Rocket):
        self.vehicle = vehicle
        self.GPS = GPS(vehicle)
        self.accelerometer = Accelerometer(vehicle)
        self.gyro = Gyroscope(vehicle)
        self.std_hor = 3.0
        self.std_vert = 7.0
        self.std_vel = .2


    def read_sensors(self):
        #gps
        measured_GPS_pos, measured_GPS_vel = self.GPS.measure(self.vehicle)

        #IMU
        measured_accel = self.accelerometer.measure()
        measured_ang_accel = self.gyro.measure()
        
        return {
            'GPS pos': measured_GPS_pos,
            'GPS vel': measured_GPS_vel,
            'IMU accel': measured_accel,
            'IMU ang accel': measured_ang_accel
        }
