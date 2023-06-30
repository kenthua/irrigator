import gpiozero
import time
import schedule

#RELAY_PIN = "BOARD16"
RELAY_PIN = 23
time1 = "06:30:00"
time2 = "21:00:00"
time3 = "03:08:10"
duration = 10

# Triggered by the output pin going high: active_hgh=True
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

def irrigate():
    try:
        print("water on")
        relay.on() 
        print(relay.value)
        time.sleep(duration)
        print("water off")
        relay.off()
        print(relay.value)
    except GPIOZeroError:
        print('A GPIO Zero error occurred')    

# set the schedule
schedule.every().monday.at(time1).do(irrigate)
schedule.every().thursday.at(time1).do(irrigate)
schedule.every().saturday.at(time1).do(irrigate)
schedule.every().friday.at(time3).do(irrigate)

while True:
    schedule.run_pending()
    time.sleep(1)