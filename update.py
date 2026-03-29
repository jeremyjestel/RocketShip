from step import step_sim
import numpy as np
def update_sim(event, sim_time, dt, rocket, physics, env, estimator, logger, sensors, ts, ball):


    sim_time += dt
    # if sim_time >= max_time:
    #     timer.stop()
    # if rocket.state.current_fuel_mass <= 0:
    #     timer.stop()
    ts = step_sim(physics, env, estimator, logger, sensors, ts)

    vispy_pos = np.array([  # position is meters so units here is 
        rocket.state.truth_pos[1] * .001,  # X_vispy = Y_sim
        rocket.state.truth_pos[0] * .001,  # Y_vispy = X_sim
        rocket.state.truth_pos[2] * .001   # Z stays same
    ])

    ball.set_data(pos=np.array([vispy_pos]), size=10)
