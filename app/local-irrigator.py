import gpiozero
import time
import schedule
import datetime
from weather import *

#RELAY_PIN = "BOARD16"
RELAY_PIN = 23
time1 = "07:00:00"
time2 = "20:30:00"
time3 = "03:08:10"
time4 = "04:25:00"
duration = 40
dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"

# Triggered by the output pin going high: active_hgh=False
# Initially off: initial_value=False
# relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

weather = Weather()

# turn the relay on and off
def irrigate():
    precipitation = weather.precipitation()
    yesterdayPrecipitation = weather.yesterdayPrecipitation()
    print("T: " + str(precipitation), flush=True)
    print("Y: " + str(yesterdayPrecipitation), flush=True)

    try:
        #print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
        #relay.on()
        fileStatus = ""
        if (precipitation <= 0.4 and yesterdayPrecipitation < 1.0): 
            print("on", flush=True)
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
            time.sleep(duration)
            print("off", flush=True)
            #print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format))
            #relay.off()
        else:
            print("rain probability", flush=True)
            fileStatus = "|| [Rain " + str(precipitation) + "] " + datetime.datetime.now().strftime(dt_format)
        file = open(filePath, "a")
        file.write(fileStatus + "\n")
        file.close()          
    except GPIOZeroError:
        print('A GPIO Zero error occurred', flush=True)
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