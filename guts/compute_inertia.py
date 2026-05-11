import numpy as np
def compute_inertia(stages, rocket_com):
    I_total = np.zeros((3, 3))

    for stage in stages:
        I_stage = stage.inertia_about_own_com()

        r = stage.com - rocket_com
        d2 = np.dot(r, r)

        parallel_axis = stage.mass * (
            d2 * np.eye(3) - np.outer(r, r)
        )

        I_total += I_stage + parallel_axis

    return I_total