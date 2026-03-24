import numpy as np
from logger import Logger


#gonna switch this to vispy
class Visualizer:
    def __init__(self, logger: Logger):
        self.logger = logger

    def plots_window(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plots

        truth_traj = np.array(self.logger.truth_positions)
        belief_traj = np.array(self.logger.belief_positions)
        time = np.array(self.logger.timestamps)

        # --- compute errors ---
        pos_error = truth_traj - belief_traj
        error_norm = np.linalg.norm(pos_error, axis=1)

        # --- figure layout ---
        fig = plt.figure(figsize=(18, 10))

        # Truth trajectory
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.plot(truth_traj[:,0], truth_traj[:,1], truth_traj[:,2])
        ax1.set_title("Rocket location truth (m)")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")
        ax1.set_xlim(truth_traj[:,0].min(), truth_traj[:,0].max())
        ax1.set_ylim(truth_traj[:,1].min(), truth_traj[:,1].max())
        ax1.set_zlim(truth_traj[:,2].min(), truth_traj[:,2].max())
        ax1.set_box_aspect([1,1,1])

        # 
        #  Belief trajectory
        ax2 = fig.add_subplot(2, 3, 2, projection='3d')
        ax2.plot(belief_traj[:,0], belief_traj[:,1], belief_traj[:,2])
        ax2.set_title("Rocket location belief (m)")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_zlabel("Z")
        ax2.set_xlim(truth_traj[:,0].min(), truth_traj[:,0].max())
        ax2.set_ylim(truth_traj[:,1].min(), truth_traj[:,1].max())
        ax2.set_zlim(truth_traj[:,2].min(), truth_traj[:,2].max())
        ax2.set_box_aspect([1,1,1])

        # Position error magnitude
        ax3 = fig.add_subplot(2, 3, 3)
        ax3.plot(time, error_norm)
        ax3.set_title("Position Error Magnitude")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Error (m)")

        # Axis-wise position error
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.plot(time, pos_error[:,0], label="X")
        ax4.plot(time, pos_error[:,1], label="Y")
        ax4.plot(time, pos_error[:,2], label="Z")
        ax4.set_title("Position Error by Axis")
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel("Error (m)")
        ax4.legend()

        # Velocity comparison (if velocities logged)
        truth_vel = np.array(self.logger.truth_vels)
        belief_vel = np.array(self.logger.belief_vels)
        ax5 = fig.add_subplot(2, 3, 5)
        ax5.plot(time, np.linalg.norm(truth_vel, axis=1), label="Truth")
        ax5.plot(time, np.linalg.norm(belief_vel, axis=1), linestyle='--', label="Belief")
        ax5.set_title("Velocity Magnitude")
        ax5.set_xlabel("Time (s)")
        ax5.set_ylabel("m/s")
        ax5.legend()

        plt.tight_layout()
        plt.show()