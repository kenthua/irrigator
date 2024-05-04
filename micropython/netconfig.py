import config
import time
from ntptime import settime

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to network...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Network Config:", wlan.ifconfig())
    print("Local time before synchronization：%s" %str(time.localtime()))
    settime()
    print("Local time after synchronization：%s" %str(time.localtime()))

#do_connect()
#print("Local time before synchronization：%s" %str(time.localtime()))
#make sure to have internet connection
#ntptime.settime()
#settime()
#print("Local time after synchronization：%s" %str(time.localtime()))
#rtc = machine.RTC()
#print(rtc.datetime())
#time.sleep_ms(500)
#print(rtc.datetime())


