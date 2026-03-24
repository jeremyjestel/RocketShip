from rocket import Rocket
import numpy as np
from GPS import GPS
from gyroscope import Gyroscope
from accelerometer import Accelerometer

class Sensor:
    def __init__(self, rocket: Rocket):
        self.rocket = rocket
        self.GPS = GPS(rocket)
        self.accelerometer = Accelerometer(rocket)
        self.gyro = Gyroscope(rocket)

    def read_sensors(self, ts):
            # GPS
            gps_pos, gps_vel, new_gps = self.GPS.measure(ts)

            gps_data = None
            if new_gps:
                gps_data = {
                    "pos": gps_pos,
                    "vel": gps_vel
                }

            # IMU
            imu_accel = self.accelerometer.measure()
            imu_gyro = self.gyro.measure()

            return {
                "imu_accel": imu_accel,
                "imu_gyro": imu_gyro,
                "gps": gps_data
            }
        
#prolly want a fuze sensors funciton down the line