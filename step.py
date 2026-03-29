import params
def step_sim(physics, env, estimator, logger, sensors, ts):
    # if rocket.state.current_fuel_mass < 0:
    #     break

    #need to update the world, then make decisions and measurements after
    physics.step_physics(env, params.dt)

    #for now not caring bout the gps 
    sensor_data = sensors.read_sensors(ts)

    #will be kalman filter but estimates from the noisy measurement
    estimator.step(sensor_data, params.dt)

    logger.log(ts)
    return ts + params.dt
