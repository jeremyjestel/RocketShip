from scipy.spatial.transform import Rotation as R
import numpy as np

class Logger:
    def __init__(self, rocket):
        self.timestamps = []
        self.truth_positions = []
        self.truth_vels = []
        self.truth_accels = []
        self.truth_ang_vels = []
        self.truth_ang_accels = []
        self.truth_orientations = []
        self.belief_positions = []
        self.belief_vels = []
        self.belief_accels = []
        self.belief_ang_vels = []
        self.belief_ang_accels = []
        self.belief_orientations = []
        self.rocket = rocket

    def log(self, ts):

        #log truth position
        self.timestamps.append(np.round(ts, decimals=1))
        self.truth_positions.append(self.rocket.state.truth_pos.copy())
        self.truth_vels.append(self.rocket.state.truth_vel.copy())
        self.truth_accels.append(self.rocket.state.truth_accel.copy())
        self.truth_ang_vels.append(self.rocket.state.truth_ang_vel.copy())
        self.truth_ang_accels.append(self.rocket.state.truth_ang_accel.copy())
        self.truth_orientations.append(R.from_quat(self.rocket.state.truth_orientation.as_quat()))

        #log final beliefs
        self.belief_positions.append(self.rocket.state.belief_pos.copy())
        self.belief_vels.append(self.rocket.state.belief_vel.copy())
        self.belief_accels.append(self.rocket.state.belief_accel.copy())
        self.belief_ang_vels.append(self.rocket.state.belief_ang_vel.copy())
        self.belief_ang_accels.append(self.rocket.state.belief_ang_accel.copy())
        self.belief_orientations.append(R.from_quat(self.rocket.state.belief_orientation.as_quat()))

    
    def print_log(self):
        for i in range(len(self.timestamps)):
            print("Timestamp: ", self.timestamps[i], ", Position Vector: ", self.truth_positions[i], ", Velocity Vector: ", self.truth_vels[i], ", Acceleration Vector: ", self.truth_accels[i])
