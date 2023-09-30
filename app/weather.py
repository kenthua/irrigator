import os
import pyowm
from pyowm.utils import timestamps, formatting

owm = pyowm.OWM(os.environ["OWM_API_KEY"])
weather_mgr = owm.weather_manager()
lat = float(os.environ["LOCATION_LAT"])
lon = float(os.environ["LOCATION_LON"])

class Weather:
    def precipitation(self):
        weather = weather_mgr.weather_at_coords(lat, lon).weather
        precipitation = Weather.convertPrecipitation(weather.precipitation_probability)
        return precipitation

    def yesterdayPrecipitation(self):
        yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
        weatherYesterday = weather_mgr.one_call_history(lat=lat, lon=lon, dt=yesterday_epoch).current
        yesterdayPrecipitation = Weather.convertPrecipitation(weatherYesterday.precipitation_probability)
        return yesterdayPrecipitation

    @staticmethod
    def convertPrecipitation(value):
        precipitation = 0.0
        if value == None:
            precipitation = 0.0
        else:
            precipitation = value
        return precipitation    
