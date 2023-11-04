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
        precipitation = Weather.convert_precipitation(weather.precipitation_probability)
        forecast3h = weather_mgr.forecast_at_coords(lat, lon, '3h').forecast
        forecast_precipitation = Weather.forecast_precipitation(forecast3h.weathers)

        # put it back in list for now
        precipitation_list = []
        precipitation_list.append(precipitation)
        precipitation_list.append(forecast_precipitation)
        highest_chance = max(precipitation_list, key=lambda x:float(x))

        return highest_chance

    def yesterdayPrecipitation(self):
        yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
        weatherYesterday = weather_mgr.one_call_history(lat=lat, lon=lon, dt=yesterday_epoch).current
        yesterdayPrecipitation = Weather.convert_precipitation(weatherYesterday.precipitation_probability)
        return yesterdayPrecipitation


    def enoughPrecipitation(self):
        status = False
        if(self.precipitation() <= 0.4 and self.yesterdayPrecipitation() < 1.0):
            status = False
        else:
            status = True
        return status

    @staticmethod
    def forecast_precipitation(weathers):
        """
        Given a list of forecast weather, grab the highest value in 12 hrs
        """
        precip = max(weathers[0:3], key=lambda w: w.precipitation_probability)
        return precip.precipitation_probability

    @staticmethod
    def convert_precipitation(value):
        precipitation = 0.0
        if value == None:
            precipitation = 0.0
        else:
            precipitation = value
        return precipitation    
