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
time4 = "04:25:00"
duration = 40
dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"

# weather
owm = pyowm.OWM(os.environ["OWM_API_KEY"])
weather_mgr = owm.weather_manager()
lat = os.environ["LOCATION_LAT"]
lon = os.environ["LOCATION_LON"]

# Triggered by the output pin going high: active_hgh=False
# Initially off: initial_value=False
# relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

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

    try:
        #print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
        #relay.on()
        fileStatus = ""
        if (precipitation <= 0.4 and yesterdayPrecipitation < 1.0): 
            print("on")
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
            time.sleep(duration)
            print("off")
            #print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
            #relay.off()
        else:
            print("rain probability")
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
        file = open(filePath, "a")
        file.write(fileStatus)
        file.close()          
    except GPIOZeroError:
        print('A GPIO Zero error occurred')
        #relay.off()
    
# set the schedule
schedule.every().monday.at(time3).do(irrigate)
schedule.every().wednesday.at(time3).do(irrigate)
schedule.every().saturday.at(time3).do(irrigate)
schedule.every().wednesday.at(time4).do(irrigate)

while True:
#    schedule.run_pending()
#    time.sleep(1)
    irrigate()