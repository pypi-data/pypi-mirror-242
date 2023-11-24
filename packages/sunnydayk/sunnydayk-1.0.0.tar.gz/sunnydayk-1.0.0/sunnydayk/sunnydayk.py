import requests


class Weather:
	"""Creates a Weather object getting an apikey as input
	and either a city name or lat and lon coordinates.

	Package use example:

	# Create a weather object using city name:
	# The api key below is not guaranteed to work.
	# Get your own apikey from https://openweathermap.org
	# And wait a coule of hours for the apikey to be activated

	>> weather1 = Weather(apikey= "***************************", city = "Saitama")
	# Using latitude and longitude coordinates
	>> weather2 = Weather(apikey= "***************************", lat = 41.1, lon = -4.1)

	# Get complete weather data for the next 12 hours:

	# Simplified data for the next 12 hours:
	>> weather1.next12h_simplified()
	"""

	def __init__(self, apikey, city=None, lat=None, lon=None):
		if city:
			url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={apikey}&units=metric"
			r = requests.get(url)
			self.data = r.json()
		elif lat and lon:
			url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apikey}&units=metric"
			r = requests.get(url)
			self.data = r.json()
		else:
			raise TypeError("provide either a city or lot and lon arguments")
		
		if self.data["cod"] != "200":
			raise ValueError(self.data["message"])


	def next_12h(self):
		"""Return 3-hours data for the next 12 hours as dict.
		"""
		return self.data['list'][:4]

	def next_12_simplified(self):
		"""Return date, temperature, and sky condition every 3 hours
		   for the next 12 hours as tuple of tuple
		"""
		simple_data = []
		for dicty in self.data['list'][:4]:
			simple_data.append((dicty['dt_txt'], dicty['main']['temp'], dicty['weather'][0]['description']))
		return simple_data


weather = Weather(apikey="c63cd20a5b33b4d03281ebbe844b0554", city="Saitama", lat=4.1, lon=4.5)

# pprint.pprint(weather.data)
# pprint.pprint(weather.next_12h())
# pprint.pprint(weather.next_12_simplified())