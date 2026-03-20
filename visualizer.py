import numpy as np
from logger import Logger

class Visualizer:
    def __init__(self, logger: Logger):
        self.logger = logger

    def plot_trajectory(self):
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plots

        truth_traj = np.array(self.logger.truth_positions)
        belief_traj = np.array(self.logger.belief_positions)

        fig = plt.figure()

        # Create 2 subplots with 3D projection
        ax1 = fig.add_subplot(1, 2, 1, projection='3d')
        ax2 = fig.add_subplot(1, 2, 2, projection='3d')

        ax1.set_xlim(truth_traj[:,0].min(), truth_traj[:,0].max())
        ax1.set_ylim(truth_traj[:,1].min(), truth_traj[:,1].max())
        ax1.set_zlim(truth_traj[:,2].min(), truth_traj[:,2].max())
        ax2.set_xlim(truth_traj[:,0].min(), truth_traj[:,0].max())
        ax2.set_ylim(truth_traj[:,1].min(), truth_traj[:,1].max())
        ax2.set_zlim(truth_traj[:,2].min(), truth_traj[:,2].max())



        # truth trajectory
        ax1.plot(truth_traj[:,0], truth_traj[:,1], truth_traj[:,2])
        ax1.set_title("Rocket location truth (m)")
        ax1.set_xlabel("X")
        ax1.set_ylabel("Y")
        ax1.set_zlabel("Z")

        # Belief trajectory
        ax2.plot(belief_traj[:,0], belief_traj[:,1], belief_traj[:,2])
        ax2.set_title("Rocket location belief (m)")
        ax2.set_xlabel("X")
        ax2.set_ylabel("Y")
        ax2.set_zlabel("Z")

        plt.show()