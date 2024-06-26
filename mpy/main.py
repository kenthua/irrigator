# import mip
# mip.install("github:peterhinch/micropython-async/v3/as_drivers/sched")
import sys
sys.path.reverse()

import json
import config
import uasyncio as asyncio
from sched.sched import schedule, Sequence
from time import localtime
from machine import Pin
import time
from umqtt.simple2 import MQTTClient
import ubinascii
import machine

relay = Pin(1,Pin.OUT)
mqtt_server = config.MQTT_SERVER
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = bytes(config.MQTT_TOPIC, "utf-8")
json_message = {}
client = MQTTClient(client_id, mqtt_server)

def irrigate():  # Demonstrate callback
    try:
        print("value: 0")
        relay.value(0)
        client.connect()
        json_message.update({"type": "irrigator"})
        json_message.update({"relay_value": str(relay.value())})
        json_message.update({"timestamp": str(time.localtime())})
        json_message.update({"device_id": config.DEVICE_ID})
        client.publish(topic_pub, json.dumps(json_message), retain=True)
        time.sleep_ms(config.DURATION)
        print("value: 1")
        relay.value(1)
        json_message.update({"relay_value": str(relay.value())})
        json_message.update({"timestamp": str(time.localtime())})
        client.publish(topic_pub, json.dumps(json_message), retain=True)
        client.disconnect()    
    except OSError as e:
        print("Irrigate Failed")
        time.sleep(2)
        client.disconnect()    
        machine.reset()

async def main():
    print("Begin scheduling...")
    try: 
        print("Set relay to 1, to turn off")
        client.connect()
        json_message.update({"type": "irrigator"})
        json_message.update({"relay_value": str("2")})
        json_message.update({"timestamp": str(time.localtime())})
        json_message.update({"device_id": config.DEVICE_ID})
        client.publish(topic_pub, json.dumps(json_message), retain=True)
        relay.value(1)
        client.disconnect()    
    except OSError as e:
        print("Main Failed")
        time.sleep(2)
        client.disconnect()    
        machine.reset()
        
    print("Set machine freq")
    machine.freq(config.MACHINE_FREQ)
    print("Machine freq: " + str(machine.freq()))
    seq = Sequence()
    print("Current time：%s" %str(time.localtime()))
    # +7 from GMT
    # wday 0-6 (mon-sun)
    asyncio.create_task(schedule(seq, 'irrigate', wday=1, hrs=14, mins=00))
    asyncio.create_task(schedule(seq, 'irrigate', wday=3, hrs=14, mins=00))
    # test
    #asyncio.create_task(schedule(seq, 'irrigate', wday=1, hrs=23, mins=52))
    print("Scheduled")
    async for args in seq:
        irrigate()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
