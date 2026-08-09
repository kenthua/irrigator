# Implementation Plan - Venus OS v3.72 DBus Upgrade

Transition the `irrigator` service from legacy `gpiozero` hardware calls to Victron's native **Venus OS DBus Relay API** (`com.victronenergy.system` `/Relay/1/State`). This resolves GPIO pin locking conflicts in Venus OS v3.60+ / v3.72, removes outdated Python dependencies, and integrates irrigation relay status directly into the Venus OS GUI and Victron VRM Portal.

## User Review Required

> [!NOTE]
> **No Hardware Rewiring Required:** Relay 2 on Venus OS DBus (`/Relay/1/State`) maps directly to physical **GPIO 2**. Your existing wiring remains unchanged.

> [!IMPORTANT]
> **Testing on Venus OS 3.55:** You can test this upgrade branch immediately on your current Venus OS v3.55 installation before performing the OS upgrade to v3.72.

---

## Proposed Changes

### Core Logic & DBus Integration

#### [irrigator.py](irrigator.py)
* Add `VenusRelay` class using Python `dbus` module to control Relay 2 (`/Relay/1/State`).
* Fallback to direct `/dev/gpio/relay_2/value` if DBus is unreachable.
* Remove `gpiozero` import and `GPIOZeroError` handling.

#### [test_irrigator.py](test_irrigator.py)
* Update unit tests to mock `VenusRelay` DBus interface instead of `gpiozero.OutputDevice`.

---

### Installer & Dependencies

#### [requirements.txt](requirements.txt)
* Remove `gpiozero`, `lgpio`, `pyowm`, `Flask` unused/incompatible packages.
* Retain `schedule==1.2.1`.

#### [install.sh](install.sh)
* Update dependency check from `gpiozero` to `schedule`.
* Remove hardcoded Python 3.8 path patch (`/usr/lib/python3.8/.../colorzero/conversions.py`).
* Update `python` commands to explicitly use `python3`.

#### [service/run](service/run)
* Update `exec python` to `exec python3`.

---

## Verification & Manual Testing Plan

### 1. Automated Unit Tests
Run local unit test suite on the repository branch:
```bash
python3 -m unittest test_irrigator.py
```

---

### 2. Manual DBus Testing Commands (On Venus OS)

Run these commands directly over SSH on your Venus OS device (`root@<VENUS-IP>`):

#### **A. Query Current Relay 2 State**
```bash
python3 -c "import dbus; bus=dbus.SystemBus(); print('Relay 2 State:', bus.get_object('com.victronenergy.system', '/Relay/1/State').GetValue())"
```

#### **B. Manual Relay ON (Toggle High)**
```bash
python3 -c "import dbus; bus=dbus.SystemBus(); bus.get_object('com.victronenergy.system', '/Relay/1/State').SetValue(dbus.Int32(1))"
```

#### **C. Manual Relay OFF (Toggle Low)**
```bash
python3 -c "import dbus; bus=dbus.SystemBus(); bus.get_object('com.victronenergy.system', '/Relay/1/State').SetValue(dbus.Int32(0))"
```

#### **D. Run 5-Second One-Shot Irrigation Test Script**
```bash
python3 -c "from irrigator import VenusRelay, irrigate; relay = VenusRelay(1); irrigate(5, relay)"
```

#### **E. Check Output & Service Logs**
```bash
# View irrigation trigger log file
cat /tmp/irrigate.out

# View daemon service log stream
tail -f /var/log/irrigator/current
```

---

### 3. Remote Service Deployment & Verification (Venus OS 3.55 & 3.72)

1. **Pull `upgrade-v3.72` branch on Venus OS:**
   ```bash
   cd /data/etc/irrigator
   git fetch origin
   git checkout upgrade-v3.72
   ```

2. **Run installer script:**
   ```bash
   bash install.sh
   ```

3. **Restart service and verify active status:**
   ```bash
   ./restart.sh
   svstat /service/irrigator
   ```
