# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import webrepl
#import webrepl_setup
webrepl.start()
from netconfig import do_connect
do_connect()

