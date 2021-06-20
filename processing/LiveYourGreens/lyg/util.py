from typing import Tuple, List

import numpy as np


def crop_layer(image: List[np.ndarray],
               x_lims: Tuple[int, int],
               y_lims: Tuple[int, int]):
    for im in image:
        im[:y_lims[0], :] = 0
        im[y_lims[1]:, :] = 0
        im[:, :x_lims[0]] = 0
        im[:, x_lims[1]:] = 0

    return image
