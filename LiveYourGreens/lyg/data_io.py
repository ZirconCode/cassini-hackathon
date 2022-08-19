from warnings import warn

import matplotlib.image as mpimg
import rasterio
from pyhdf.SD import SD, SDC

from .constants import BOUNDS

class LayerReader:
    """
    Read EO data sets.
    """

    def __init__(self):
        self.m_layers = {}
        self.m_bounds = {}

    def read_geotiff(self, layer_name: str, input_path: str):
        image = rasterio.open(input_path).read()
        self.m_layers[layer_name] = image
        self.m_bounds[layer_name] = BOUNDS

    def read_image(self, layer_name: str, input_path: str):
        image = mpimg.imread(input_path)
        self.m_layers[layer_name] = image
        self.m_bounds[layer_name] = BOUNDS

    def read_hdf4(self, layer_name: str, input_path):
        file = SD(input_path, SDC.READ)
        image = file.select(layer_name).get()
        self.m_layers[layer_name] = image
        self.m_bounds[layer_name] = BOUNDS

    def overwrite_warning(self, layer_name):
        if layer_name in self.m_layers.keys():
            warn("Layer is being overwritten")
