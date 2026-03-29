from init_vis import init_vis
from step import step_sim
import numpy as np
from vispy.app import Timer
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
        self.canvas, self.view, self.ball = init_vis()
        self.timer = Timer(self.dt, connect=self.update, start=True)

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
            self.rocket.state.truth_pos[1], 
            self.rocket.state.truth_pos[0], 
            self.rocket.state.truth_pos[2]
        ])
        self.view.camera.center = vispy_pos
        self.ball.set_data(pos=np.array([vispy_pos]), size=25)