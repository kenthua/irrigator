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

## Verification Plan

### Automated Unit Tests
Run local unit test suite on the new branch:
```bash
python3 -m unittest test_irrigator.py
```

### Remote Verification on Venus OS 3.55 (`192.168.4.74`)
1. Pull `upgrade-v3.72` branch on Venus OS:
   ```bash
   cd /data/etc/irrigator
   git fetch origin
   git checkout upgrade-v3.72
   bash install.sh
   ```
2. Verify relay toggle via DBus:
   ```bash
   python3 -c "import dbus; bus=dbus.SystemBus(); print('Relay 2:', bus.get_object('com.victronenergy.system', '/Relay/1/State').GetValue())"
   ```
3. Restart service and check status:
   ```bash
   ./restart.sh
   svstat /service/irrigator
   tail -n 20 /var/log/irrigator/current
   ```
