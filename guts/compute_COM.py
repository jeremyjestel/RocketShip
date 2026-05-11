from guts.compute_total_mass import compute_total_mass
import numpy as np


def compute_COM(stages) -> np.ndarray:
    total_mass = compute_total_mass(stages)
    weighted_sum = np.zeros(3)

    for stage in stages:
        weighted_sum += stage.mass * stage.com

    return weighted_sum / total_mass
