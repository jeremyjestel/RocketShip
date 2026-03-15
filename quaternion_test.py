import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

# --- create a 30 degree rotation around X axis (pitch) ---
angle = np.deg2rad(45)
axis = np.array([0, 1, 0])

orientation = R.from_euler('x', 30, degrees=True) # x or y or z for pitch roll yaw

rocket_forward_body = np.array([0,0,1])
rocket_forward_world = orientation.apply(rocket_forward_body)

print("Rocket forward direction in world frame:")
print(rocket_forward_world)

# --- visualize ---
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# world up vector
ax.quiver(0,0,0,0,0,1,length=1, label="World Up")

# rocket direction
ax.quiver(0,0,0,
          rocket_forward_world[0],
          rocket_forward_world[1],
          rocket_forward_world[2],
          length=1, label="Rocket Nose")

ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
ax.set_zlim([0,1.2])

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

plt.legend()
plt.show()