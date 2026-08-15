import time
import schedule
import datetime
import os

try:
    import dbus
    HAS_DBUS = True
except ImportError:
    HAS_DBUS = False


class VenusRelay:
    """Controls a Victron Venus OS relay pin via DBus with sysfs file fallback."""

    def __init__(self, relay_index=1, sysfs_path="/dev/gpio/relay_2/value"):
        self.relay_index = relay_index
        self.sysfs_path = sysfs_path

        if HAS_DBUS:
            try:
                self.bus = dbus.SystemBus()
                self.path = f"/Relay/{self.relay_index}/State"
                self.obj = self.bus.get_object("com.victronenergy.system", self.path)
                self.iface = dbus.Interface(self.obj, "com.victronenergy.BusItem")
                self.use_dbus = True
            except Exception as e:
                print(f"DBus initialization failed ({e}), falling back to sysfs", flush=True)
                self.use_dbus = False
        else:
            self.use_dbus = False

    def on(self):
        if self.use_dbus:
            self.iface.SetValue(dbus.Int32(1))
        elif os.path.exists(self.sysfs_path):
            with open(self.sysfs_path, "w") as f:
                f.write("1")

    def off(self):
        if self.use_dbus:
            self.iface.SetValue(dbus.Int32(0))
        elif os.path.exists(self.sysfs_path):
            with open(self.sysfs_path, "w") as f:
                f.write("0")

    @property
    def value(self):
        if self.use_dbus:
            return int(self.iface.GetValue())
        elif os.path.exists(self.sysfs_path):
            with open(self.sysfs_path, "r") as f:
                val = f.read().strip()
                return int(val) if val.isdigit() else 0
        return 0


# Configuration
RELAY_INDEX = 1  # 0 = Relay 1 (GPIO 21), 1 = Relay 2 (GPIO 2)
time1 = "17:30:00"
time2 = "20:30:00"
time3 = "04:06:00"
duration = 60
dt_format = "%Y-%m-%d %H:%M:%S"
filePath = "/tmp/irrigate.out"


def get_timestamp():
    return datetime.datetime.now().strftime(dt_format)


def irrigate(duration, relay):
    """Executes a timed irrigation cycle safely, ensuring the relay turns off under all circumstances."""
    print(f"[{get_timestamp()}] WATER ON | Relay State: {relay.value}", flush=True)

    try:
        relay.on()
        time.sleep(duration)
    except Exception as e:
        print(f"[{get_timestamp()}] ERROR during irrigation: {e}", flush=True)
    finally:
        # Guarantee relay is shut off regardless of any errors or interrupts
        relay.off()
        end_time = get_timestamp()
        print(f"[{end_time}] WATER OFF | Relay State: {relay.value}", flush=True)

        # Log completion record for Web UI history
        try:
            with open(filePath, "a") as f:
                f.write(f"|| {end_time}\n")
        except IOError as err:
            print(f"[{end_time}] Failed to write log history to {filePath}: {err}", flush=True)


if __name__ == "__main__":
    relay = VenusRelay(relay_index=RELAY_INDEX)

    # Set schedule (Tuesdays, Thursdays, Sundays at 17:30)
    schedule.every().tuesday.at(time1).do(irrigate, duration, relay)
    schedule.every().thursday.at(time1).do(irrigate, duration, relay)
    schedule.every().sunday.at(time1).do(irrigate, duration, relay)

    while True:
        schedule.run_pending()
        time.sleep(1)
