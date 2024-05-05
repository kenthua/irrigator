# import mip
# mip.install("github:peterhinch/micropython-async/v3/as_drivers/sched")
import sys
sys.path.reverse()

import config
import uasyncio as asyncio
from sched.sched import schedule, Sequence
from time import localtime
from machine import Pin
import time
from umqtt.simple2 import MQTTClient
import ubinascii
import machine

relay = Pin(13,Pin.OUT)
mqtt_server = config.MQTT_SERVER
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'esp32'

def irrigate():  # Demonstrate callback
    try:
        print("value: 0")
        relay.value(0)
        client = MQTTClient(client_id, mqtt_server)
        client.connect()
        message = "Irrigator: [" + str(relay.value()) + "]: " + str(time.localtime())
        client.publish(topic_pub, message, retain=True)
        client.disconnect()    
        time.sleep_ms(config.DURATION)
        print("value: 1")
        relay.value(1)
    except OSError as e:
        print("Failed")
        time.sleep(2)
        machine.reset()

async def main():
    print("Begin scheduling...")
    print("Set relay to 1, to turn off")
    relay.value(1)
    seq = Sequence()
    print("Current time：%s" %str(time.localtime()))
    # +7 from GMT
    # wday 0-6 (mon-sun)
    asyncio.create_task(schedule(seq, 'irrigate', wday=1, hrs=14, mins=00))
    asyncio.create_task(schedule(seq, 'irrigate', wday=3, hrs=14, mins=00))
    print("Scheduled")
    async for args in seq:
        irrigate()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
