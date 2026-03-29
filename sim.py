from init_vis import init_vis
from step import step_sim
import numpy as np
from vispy.app import Timer
from vispy.visuals.transforms import MatrixTransform
from vispy.scene.visuals import Line

class Sim:
    def __init__(self, rocket, physics, env, estimator, logger, sensors, dt, max_time):
        self.rocket = rocket
        self.physics = physics
        self.env = env
        self.estimator = estimator
        self.logger = logger
        self.sensors = sensors
        self.ts = 0.0
        self.sim_time = 0.0
        self.dt = dt
        self.max_time = max_time
        self.canvas, self.view, self.vis_rocket, self.labels = init_vis(rocket.state.truth_pos)
        self.timer = Timer(self.dt, connect=self.update, start=True)
        self.axis_len = 0.3

        vispy_pos = np.array([
            self.rocket.state.truth_pos[0], 
            self.rocket.state.truth_pos[1], 
            self.rocket.state.truth_pos[2]
        ])

        R = self.rocket.state.truth_orientation.as_matrix()  # shape (3,3)

        self.roll_axis   = R @ np.array([self.axis_len, 0, 0])
        self.pitch_axis      = R @ np.array([0, self.axis_len, 0])
        self.forward_axis = R @ np.array([0, 0, self.axis_len])

        self.line_x = Line(pos=np.array([vispy_pos - self.roll_axis, vispy_pos + self.roll_axis]), color='blue')
        self.line_y = Line(pos=np.array([vispy_pos - self.pitch_axis, vispy_pos + self.pitch_axis]), color='green')
        self.line_z = Line(pos=np.array([vispy_pos - self.forward_axis, vispy_pos + self.forward_axis]), color='red')


    def update(self, event):

        self.sim_time += self.dt
        if self.sim_time >= self.max_time:
            self.timer.stop()
        
        if self.rocket.state.current_fuel_mass <= 0:
            self.rocket.engine.thrust_vec = np.array([0,0,0]) 

        if self.rocket.state.truth_pos[2] <= 0 and self.sim_time >= 1:
            self.timer.stop()

        self.ts = step_sim(
            self.physics,
            self.env,
            self.estimator,
            self.logger,
            self.sensors,
            self.ts
        )

        vispy_pos = np.array([
            self.rocket.state.truth_pos[0], 
            self.rocket.state.truth_pos[1], 
            self.rocket.state.truth_pos[2]
        ])
        self.labels[0].text = f'X: {vispy_pos[0]:.2f}'
        self.labels[1].text = f'Y: {vispy_pos[1]:.2f}'
        self.labels[2].text = f'Z: {vispy_pos[2]:.2f}'

        euler_angles = self.rocket.state.truth_orientation.as_euler('xyz', degrees=True)
        pitch, yaw, roll = euler_angles  # in degrees
        self.labels[3].text = f"Pitch: {pitch:.1f}°\n Yaw: {yaw:.1f}°\n Roll: {roll:.1f}°"



        #follow the rocket with camera
        self.view.camera.center = vispy_pos

        #remove prior transforms
        self.vis_rocket.transform.reset()  # VERY IMPORTANT

        # Get 3x3 rotation matrix from scipy Rotation
        # Apply rotation
        self.vis_rocket.transform.matrix[:3, :3] = self.rocket.state.truth_orientation.as_matrix()

        #move the rocket to the truth position
        self.vis_rocket.transform.translate(vispy_pos)

        #Add axis lines for rocket frame
        self.line_x.parent = None
        self.line_y.parent = None
        self.line_z.parent = None

        #define ends of the lines for each plane
        R = self.rocket.state.truth_orientation.as_matrix()  # shape (3,3)
        self.roll_axis    = R @ np.array([self.axis_len, 0, 0])
        self.pitch_axis   = R @ np.array([0, self.axis_len, 0])
        self.forward_axis = R @ np.array([0, 0, self.axis_len])

        #update each line
        self.line_x.set_data(pos=np.array([vispy_pos - self.roll_axis, vispy_pos + self.roll_axis]))
        self.line_y.set_data(pos=np.array([vispy_pos - self.pitch_axis, vispy_pos + self.pitch_axis]))
        self.line_z.set_data(pos=np.array([vispy_pos - self.forward_axis, vispy_pos + self.forward_axis]))

        # add lines to the visual view
        self.view.add(self.line_x)
        self.view.add(self.line_y)
        self.view.add(self.line_z)

