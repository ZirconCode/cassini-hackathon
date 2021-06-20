import lyg


class WebsiteGetter(object):
	def __init__(self,
				 input_path):
		self.green = lyg.GreenMetric(bounds={'west': 8.258889841,
											 'north': 47.562982412,
											 'south': 47.235039561,
											 'east': 8.738077426})

		self.green.load_metric(input_path=input_path,
							   resolution=(1704, 4018))

	def get(self,
			lon,
			lat):
		return self.green.get_metric(lon=lon,
									 lat=lat)
