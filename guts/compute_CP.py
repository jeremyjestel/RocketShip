import numpy as np


def compute_CP(stages) -> np.ndarray:
    weighted_sum = np.zeros(3)
    total_weight = 0.0

    for stage in stages:
        area = np.pi * stage.radius**2
        weight = area * stage.normal_force_coeff

        weighted_sum += weight * stage.aero_center
        total_weight += weight

    return weighted_sum / total_weight
