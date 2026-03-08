from rocket import Rocket
import numpy as np

# Create a rocket with default parameters Only need one for sim

my_rocket = Rocket(name="JermTest")

#base params
current_timestep = 0
dt = .01 #seconds
sim_time = 10

print(my_rocket)


while current_timestep < sim_time:
    current_timestep += dt



print("success")