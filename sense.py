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

    def read_sensors(self, ts, dt):
        #gps
        measured_GPS_pos, measured_GPS_vel = self.GPS.measure(ts)

        #IMU
        self.vehicle.state.belief_accel = self.accelerometer.measure()
        self.vehicle.state.belief_ang_accel = self.gyro.measure()

        self.vehicle.state.update_belief_state(dt)
        
#prolly want a fuze sensors funciton down the line