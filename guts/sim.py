from UI.init_vis import init_vis
from UI.input_handler import InputHandler
from guts.step import step_sim
import numpy as np
from typing import Any, cast
from vispy.app import Timer
from vispy.visuals.transforms import MatrixTransform
from vispy.scene.visuals import Line, Markers
from scipy.spatial.transform import Rotation as R
import params
from vispy.scene import Text
from UI.panel import Panel



class Sim:
    def __init__(self, rocket, physics, env, estimator, logger, sensors, dt, max_time, session_end_callback=None):
        self.rocket = rocket
        self.dt = dt
        self.canvas, self.view, self.vis_rocket = init_vis(rocket.state.truth_pos)
        self.canvas = cast(Any, self.canvas)
        self.input_handler = InputHandler(rocket)
        self.paused = False
        self.session_end_callback = session_end_callback
        self.session_active = False

        # Connect keyboard events
        self.canvas.events.key_press.connect(self.input_handler.on_key_press)
        self.canvas.events.key_release.connect(self.input_handler.on_key_release)

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

        self.line_x = Line(pos=np.array([vispy_pos - self.roll_axis, vispy_pos + self.roll_axis]), color='red')
        self.line_y = Line(pos=np.array([vispy_pos - self.pitch_axis, vispy_pos + self.pitch_axis]), color='blue')
        self.line_z = Line(pos=np.array([vispy_pos - self.forward_axis, vispy_pos + self.forward_axis]), color='green')
        self.line_x.set_gl_state(depth_test=False)
        self.line_y.set_gl_state(depth_test=False)
        self.line_z.set_gl_state(depth_test=False)

        self.trail_positions = [vispy_pos.copy()]
        self.trail = Markers(parent=self.view.scene)
        self.trail.set_gl_state(depth_test=False)
        self.trail.set_data(
            np.array(self.trail_positions),
            face_color='yellow',
            edge_color='yellow',
            edge_width=0.0,
            size=5,
        )

        self.telemetry = Panel(rocket, pause_callback=self.toggle_pause, close_callback=self.end_session)
        canvas_native = getattr(self.canvas, "native", None)
        if canvas_native is not None:
            canvas_native.closeEvent = self._handle_canvas_close
        self.telemetry.show()
        self.reset_session(rocket, physics, env, estimator, logger, sensors, dt, max_time)

    def reset_session(self, rocket, physics, env, estimator, logger, sensors, dt, max_time):
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
        self.paused = False
        self.session_active = True

        self.input_handler.rocket = rocket
        for key in self.input_handler.key_state:
            self.input_handler.key_state[key] = False

        self.telemetry.set_context(rocket, pause_callback=self.toggle_pause)
        self.telemetry.show()
        self._show_canvas()

        vispy_pos = np.array([
            self.rocket.state.truth_pos[0],
            self.rocket.state.truth_pos[1],
            self.rocket.state.truth_pos[2]
        ])

        self.trail_positions = [vispy_pos.copy()]
        self.trail.set_data(
            np.array(self.trail_positions),
            face_color='yellow',
            edge_color='yellow',
            edge_width=0.0,
            size=5,
        )
        self.view.camera.center = vispy_pos
        self._update_visuals(vispy_pos)

        self.timer.stop()
        self.timer.interval = self.dt
        self.timer.start()

    def toggle_pause(self):
        self.paused = not self.paused
        return self.paused

    def _handle_canvas_close(self, event):
        self.end_session()
        event.ignore()

    def _show_canvas(self):
        canvas_native = getattr(self.canvas, "native", None)
        if canvas_native is not None:
            canvas_native.show()
            canvas_native.raise_()
            canvas_native.activateWindow()
            return
        self.canvas.show()

    def _hide_canvas(self):
        canvas_native = getattr(self.canvas, "native", None)
        if canvas_native is not None:
            canvas_native.hide()
            return
        self.canvas.close()

    def end_session(self):
        if not self.session_active:
            return

        self.session_active = False
        self.finish_run()
        self.telemetry.hide()
        self._hide_canvas()

        if self.session_end_callback is not None:
            self.session_end_callback()

    def _update_visuals(self, vispy_pos):
        self.vis_rocket.transform.reset()
        self.vis_rocket.transform.matrix[:3, :3] = self.rocket.state.truth_orientation.inv().as_matrix()
        self.vis_rocket.transform.translate(vispy_pos)

        rotation_matrix = self.rocket.state.truth_orientation.as_matrix()
        self.roll_axis = rotation_matrix @ np.array([self.axis_len, 0, 0])
        self.pitch_axis = rotation_matrix @ np.array([0, self.axis_len, 0])
        self.forward_axis = rotation_matrix @ np.array([0, 0, self.axis_len])

        self.line_x.set_data(pos=np.array([vispy_pos - self.roll_axis, vispy_pos + self.roll_axis]))
        self.line_y.set_data(pos=np.array([vispy_pos - self.pitch_axis, vispy_pos + self.pitch_axis]))
        self.line_z.set_data(pos=np.array([vispy_pos - self.forward_axis, vispy_pos + self.forward_axis]))

        self.line_x.parent = self.view.scene
        self.line_y.parent = self.view.scene
        self.line_z.parent = self.view.scene

    def finish_run(self):
        self.timer.stop()

    def update(self, event):



        if self.rocket.state.current_fuel_mass <= 0:
            self.rocket.engine.thrust_vec = np.array([0,0,0]) 

        # Apply keyboard controls
        self.input_handler.apply_controls()

        if not self.paused:
            self.ts = step_sim(
                self.physics,
                self.env,
                self.estimator,
                self.logger,
                self.sensors,
                self.ts
            )
            self.sim_time += self.dt

        if self.sim_time >= self.max_time:
            self.finish_run()
            return

        self.telemetry.update_display(self.sim_time)

        vispy_pos = np.array([
            self.rocket.state.truth_pos[0], 
            self.rocket.state.truth_pos[1], 
            self.rocket.state.truth_pos[2]
        ])
        
        # Keep following the rocket only while the sim is running.
        if not self.paused:
            self.view.camera.center = vispy_pos
            self.trail_positions.append(vispy_pos.copy())
            self.trail.set_data(
                np.array(self.trail_positions),
                face_color='yellow',
                edge_color='yellow',
                edge_width=0.0,
                size=5,
            )

        # self.labels[0].text = f'X: {vispy_pos[0]:.2f}'
        # self.labels[1].text = f'Y: {vispy_pos[1]:.2f}'
        # self.labels[2].text = f'Z: {vispy_pos[2]:.2f}'

        # euler_angles = self.rocket.state.truth_orientation.as_euler('xyz', degrees=True)
        # pitch, yaw, roll = euler_angles  # in degrees
        # self.labels[3].text = f"Pitch: {pitch:.1f}°\n Yaw: {yaw:.1f}°\n Roll: {roll:.1f}°"
        # self.labels[4].text = f'Time: {self.sim_time:.2f}'




        self._update_visuals(vispy_pos)


        #ugh velocity cant be going down if rocket hasnt left the ground,
        if self.rocket.state.truth_pos[2] <= -.001 and self.rocket.state.in_flight == True:            
            self.finish_run()
            return
