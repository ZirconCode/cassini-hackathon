from .green_metric import GreenMetric
from .constants import BOUNDS


class WebsiteGetter:
    def __init__(self, input_path):
        self.green = GreenMetric(bounds=BOUNDS)
        self.green.load_metric(input_path=input_path, resolution=(1704, 4018))

    def get(self, lat, lon):
        return self.green.get_metric(lat, lon)
