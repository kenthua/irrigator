import gpiozero
import time

#RELAY_PIN = "BOARD16"
RELAY_PIN = 23

# Triggered by the output pin going high: active_high=True
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=False)

relay.on() 
print(relay.value)
time.sleep(5)
relay.off()

print(relay.value)