import gpiozero
import time
import schedule
import datetime

from gpiozero import GPIOZeroError

#RELAY_PIN = "BOARD16"
RELAY_PIN = 2
time1 = "17:30:00"
time2 = "20:30:00"
time3 = "03:08:10"
duration = 20
dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"

# Triggered by the output pin going high: active_hugh=True (for single relay, False for 4xrelay)
# Initially off: initial_value=False
relay = gpiozero.OutputDevice(RELAY_PIN, active_high=True, initial_value=False)

# turn the relay on and off
def irrigate():
    try:
        fileStatus = ""
        print("water on " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
        relay.on()
        fileStatus = "|| " + datetime.datetime.now().strftime(dt_format)
        time.sleep(duration)
        print("water off " + str(relay.value) + " " + datetime.datetime.now().strftime(dt_format), flush=True)
        relay.off()

        file = open(filePath, "a")
        file.write(fileStatus + "\n")
        file.close()
    except GPIOZeroError:
        print('A GPIO Zero error occurred', flush=True)
        relay.off()
    
# set the schedule
schedule.every().tuesday.at(time1).do(irrigate)
schedule.every().thursday.at(time1).do(irrigate)
#schedule.every().friday.at(time1).do(irrigate)
#schedule.every().saturday.at(time1).do(irrigate)

while True:
    schedule.run_pending()
    time.sleep(1)
