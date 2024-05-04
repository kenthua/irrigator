# import mip
# mip.install("github:peterhinch/micropython-async/v3/as_drivers/sched")
import sys
sys.path.reverse()

import uasyncio as asyncio
from sched.sched import schedule, Sequence
from time import localtime
from machine import Pin
import time
from umqtt.simple2 import MQTTClient
import ubinascii
import machine

p2 = Pin(2,Pin.OUT)
mqtt_server = "192.168.4.11"
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'esp32'

def irrigate():  # Demonstrate callback
    print("on")
    try:
        p2.on()
        client = MQTTClient(client_id, mqtt_server)
        client.connect()
        message = "Irrigator: " + str(time.localtime())
        client.publish(topic_pub, message, retain=True)
        client.disconnect()    
        time.sleep_ms(500)
        print("off")
        p2.off()
    except OSError as e:
        print("Failed")
        time.sleep(2)
        machine.reset()

async def main():
    print("Begin scheduling...")
    seq = Sequence()
    print("Current time：%s" %str(time.localtime()))
    # +7 from GMT
    # wday 0-6 (mon-sun)
    asyncio.create_task(schedule(seq, 'irrigate', wday=5, hrs=22, mins=48))
    print("Scheduled")
    async for args in seq:
        irrigate()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()