from typing import Tuple
from warnings import warn

import numpy as np
from tqdm import tqdm
from skimage.measure import block_reduce
from skimage.filters import gaussian

from lyg.util import crop_layer


class GreenMetric(object):
    def __init__(self,
                 bounds: dict):
        self.m_streets = None
        self.m_street_locs = None
        self.m_green_distance_index = None
        self.m_resolution = None
        self.m_xmap = None
        self.m_ymap = None
        self.m_xmap_cood = None
        self.m_ymap_cood = None
        self.m_bounds = bounds
        self.m_metric = None

    def get_metric(self, lat, lon):
        if self.m_xmap_cood is None:
            self.create_maps()
        if ((lat < self.m_bounds['south']) or (lat > self.m_bounds['north'])
                or (lon < self.m_bounds['west']) or (lon > self.m_bounds['east'])):
            warn('Value requested lies outside of map')
            return 0

        x = np.argmin(np.abs(self.m_xmap_cood - lon))
        y = np.argmin(np.abs(self.m_ymap_cood - lat))

        return self.m_metric[y, x]

    def green_distance_index(self,
                             ndv_index: np.ndarray,
                             threshhold: float,
                             cutoff_dist: int,
                             reduce_factor: float):

        if self.m_streets is None:
            raise ValueError('No streets loaded')

        self.check_resolution(ndv_index)

        if self.m_xmap is None:
            self.create_maps()

        self.m_green_distance_index = np.zeros_like(ndv_index)

        ndv_index[ndv_index < threshhold] = 0

        # normalize image
        ndv_index -= np.min(ndv_index)
        ndv_index = ndv_index / np.max(ndv_index)

        ndv_reduce = block_reduce(ndv_index, block_size=(reduce_factor, reduce_factor),
                                  func=np.mean, cval=0)
        reduce_pos_x = np.transpose(
            np.tile(np.linspace(start=0 + reduce_factor/2,
                                stop=self.m_resolution[1] - reduce_factor/2,
                                num=ndv_reduce.shape[1]),
                    (ndv_reduce.shape[0], 1)))
        reduce_pos_y = np.tile(np.linspace(start=0 + reduce_factor/2,
                                           stop=self.m_resolution[0] - reduce_factor/2,
                                           num=ndv_reduce.shape[0]),
                               (ndv_reduce.shape[1], 1))

        x = []
        y = []
        value = []

        for i in range(ndv_reduce.shape[0]):
            for j in range(ndv_reduce.shape[1]):
                x.append(reduce_pos_x[j, i])
                y.append(reduce_pos_y[j, i])
                value.append(ndv_reduce[i, j])

        x = np.array(x)
        y = np.array(y)
        value = np.array(value)

        for pos in tqdm(self.m_street_locs):
            # cropped = crop_layer(image=[ndv_index, self.m_xmap, self.m_ymap],
            #                      x_lims=(pos[0]-cutoff_dist, pos[0]+cutoff_dist),
            #                      y_lims=(pos[1]-cutoff_dist, pos[1]+cutoff_dist))
            #
            # ndv_crop = cropped[0]
            # x_c = cropped[1]
            # y_c = cropped[2]
            # distance = np.sqrt((x_c - pos[0]) ** 2 + (y_c - pos[1]) ** 2)

            distance = np.sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2)

            self.m_green_distance_index[pos[1], pos[0]] = np.sum(value / distance)

    def load_streets(self,
                     streets: np.ndarray,
                     x_lims: Tuple[int, int],
                     y_lims: Tuple[int, int]):

        self.check_resolution(streets)
        streets -= streets.min()
        streets /= streets.max()
        streets = np.round(streets)
        streets = np.invert(streets.astype(bool)).astype(float)

        streets = crop_layer(image=[streets],
                             x_lims=x_lims,
                             y_lims=y_lims)[0]

        self.m_streets = streets
        self.m_street_locs = list(zip(np.where(streets == 1)[1], np.where(streets == 1)[0]))

    def combine_metric(self):
        green = self.m_green_distance_index
        green = green / np.max(green)
        green = green * 100
        green = gaussian(green, sigma=5)

        self.m_metric = green

    def save_metric(self,
                    output_path: str):
        np.save(file=output_path,
                arr=self.m_metric)

    def load_metric(self,
                    input_path,
                    resolution):
        self.m_metric = np.load(file=input_path)
        self.m_resolution = resolution

    def check_resolution(self,
                         image):
        if self.m_resolution is not None:
            if ((image.shape[0] != self.m_resolution[0])
                    or (image.shape[1] != self.m_resolution[1])):
                raise ValueError('Resolution mismatch')
        else:
            self.m_resolution = image.shape

    def create_maps(self):
        self.m_xmap = np.transpose(np.tile(np.arange(-self.m_resolution[1] / 2,
                                                     self.m_resolution[1] / 2),
                                           (self.m_resolution[0], 1)))
        self.m_ymap = np.tile(np.arange(
            -self.m_resolution[0] / 2,
            self.m_resolution[0] / 2),
            (self.m_resolution[1], 1))

        ew_pix = (self.m_bounds['east'] - self.m_bounds['west'])/self.m_resolution[1]
        ns_pix = (self.m_bounds['north'] - self.m_bounds['south'])/self.m_resolution[0]

        self.m_ymap_cood = np.linspace(
            start=self.m_bounds['south']+ns_pix/2,
            stop=self.m_bounds['north']-ns_pix/2,
            num=self.m_resolution[0])
        self.m_xmap_cood = np.linspace(start=self.m_bounds['west']+ew_pix/2,
                                       stop=self.m_bounds['east']+ew_pix/2,
                                       num=self.m_resolution[1],
                                       endpoint=True)
