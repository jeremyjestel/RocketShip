import numpy as np
from logger import Logger

class Visualizer:
    def __init__(self, logger: Logger):
        self.logger = logger

    def plot_trajectory(self):
        import matplotlib.pyplot as plt
        traj = np.array(self.logger.positions)
        if traj.shape[0] == 0:
            print("No data to plot.")
            return
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(traj[:,0], traj[:,1], traj[:,2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()