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

relay = Pin(config.RELAY_PIN, Pin.OUT)
mqtt_server = config.MQTT_SERVER
client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = bytes(config.MQTT_TOPIC, "utf-8")
#json_message = {}
client = MQTTClient(client_id, mqtt_server)

def prepareMessage(relay_state):
    json_message = {}
    json_message.update({"type": "irrigator"})
    json_message.update({"relay_value": str(relay_state)})
    json_message.update({"timestamp": str(time.localtime())})
    json_message.update({"device_id": config.DEVICE_ID})    
    return json_message

def irrigate():  # Demonstrate callback
    try:
        print(f"value: {config.RELAY_ON}")
        relay.value(config.RELAY_ON)
        client.connect()
        _json_message = prepareMessage(relay.value())
        client.publish(topic_pub, json.dumps(_json_message), retain=True)
        time.sleep_ms(config.DURATION)
        print(f"value: {config.RELAY_OFF}")
        relay.value(config.RELAY_OFF)
        _json_message = prepareMessage(relay.value())
        client.publish(topic_pub, json.dumps(_json_message), retain=True)
        client.disconnect()
    except OSError as e:
        print("Irrigate Failed")
        time.sleep(2)
        client.disconnect()    
        machine.reset()

async def main():
    print("Begin scheduling...")
    print(f"Relay Pin Configured to: {config.RELAY_PIN}")
    try: 
        print(f"Set relay to off: {config.RELAY_OFF}")
        client.connect()
        _json_message = prepareMessage(config.RELAY_INIT)
        client.publish(topic_pub, json.dumps(_json_message), retain=True)
        relay.value(config.RELAY_OFF)
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
    asyncio.create_task(schedule(seq, 'irrigate', wday=6, hrs=17, mins=51))
    print("Scheduled")
    async for args in seq:
        irrigate()

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
