import gpiozero
import time
import schedule
import datetime
import pyowm
from pyowm.utils import timestamps, formatting
import os

#RELAY_PIN = "BOARD16"
RELAY_PIN = 23
time1 = "07:00:00"
time2 = "20:30:00"
time3 = "03:08:10"
duration = 45
dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"

# weather
owm = pyowm.OWM(os.environ["OWM_API_KEY"])
weather_mgr = owm.weather_manager()
lat = float(os.environ["LOCATION_LAT"])
lon = float(os.environ["LOCATION_LON"])

# Triggered by the output pin going high: active_hgh=False
# Initially off: initial_value=False
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

def convertPrecipitation(value):
    precipitation = 0.0
    if value == None:
        precipitation = 0.0
    else:
        precipitation = value
    return precipitation    

# turn the relay on and off
def irrigate():
    weather = weather_mgr.weather_at_coords(lat, lon).weather
    yesterday_epoch = formatting.to_UNIXtime(timestamps.yesterday())
    weatherYesterday = weather_mgr.one_call_history(lat=lat, lon=lon, dt=yesterday_epoch).current

    precipitation = convertPrecipitation(weather.precipitation_probability)
    yesterdayPrecipitation = convertPrecipitation(weatherYesterday.precipitation_probability)
    print("T: " + str(precipitation), flush=True)
    print("Y: " + str(yesterdayPrecipitation), flush=True)

    try:
        fileStatus = ""
        if (precipitation <= 0.4 and yesterdayPrecipitation < 1.0): 
            print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            relay.on()
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
            time.sleep(duration)
            print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            relay.off()
        else:
            print("rain probability " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
        
        file = open(filePath, "a")
        file.write(fileStatus + "\n")
        file.close()
    except GPIOZeroError:
        print('A GPIO Zero error occurred', flush=True)
        relay.off()
    
# set the schedule
schedule.every().monday.at(time1).do(irrigate)
schedule.every().wednesday.at(time1).do(irrigate)
schedule.every().friday.at(time1).do(irrigate)
#schedule.every().saturday.at(time1).do(irrigate)

while True:
    schedule.run_pending()
    time.sleep(1)