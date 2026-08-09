# Victron Venus OS Irrigator Service

Automated irrigation controller designed to run as a native supervised background service on **Victron Venus OS** (Raspberry Pi / Cerbo GX).

---

## 🌟 Overview

The `irrigator` service controls an external water valve/pump connected to a relay (GPIO pin) on a Victron Venus OS device. It utilizes Venus OS's built-in `daemontools` service manager for daemon supervision and auto-restarting, while ensuring installation persistence across Venus OS firmware upgrades.

Key features:
* **Native Venus OS Service:** Supervised via `daemontools` (`/service/irrigator`).
* **Firmware Update Persistent:** Installs in `/data/etc/irrigator` and hooks into `/data/rc.local` so system re-flashes do not remove the service.
* **Scheduled Irrigation:** Uses Python's `schedule` and `gpiozero` modules for time-based relay activation.
* **Integrated Logging:** Managed by `multilog` to `/var/log/irrigator`.

---

## 📅 Default Schedule & Configuration

The irrigation schedule and pin assignment are configured in `irrigator.py`:

* **Relay Pin:** `GPIO 2` (`RELAY_PIN = 2`, Active High)
* **Schedule:**
  * **Days:** Every **Tuesday**, **Thursday**, and **Sunday**
  * **Start Time:** `17:30:00` (5:30 PM)
  * **Duration:** `60` seconds
* **Execution Log:** `/tmp/irrigate.out` and `/var/log/irrigator`

---

## 🛠️ Installation Instructions

### Prerequisites
* Victron Venus OS running on Raspberry Pi or similar hardware.
* Root SSH access enabled (**Settings > General > Access Level** set to *Superuser*, SSH enabled).

### Quick Install (Via SSH)

1. **SSH into your Venus OS device:**
   ```bash
   ssh root@<YOUR-VENUS-OS-IP>
   ```

2. **Clone the repository to persistent storage (`/data`):**
   ```bash
   mkdir -p /data/etc
   cd /data/etc
   git clone https://github.com/kenthua/irrigator.git
   cd /data/etc/irrigator
   ```

3. **Run the installation script:**
   ```bash
   bash install.sh
   ```

---

## 🔍 How Installation & Auto-Persistence Work

When `install.sh` runs, it automatically handles system setup and persistence:

1. **Permissions:** Sets executable permissions (`chmod 755`) on python scripts, installer scripts, and `service/run` hooks.
2. **Dependencies:** Checks for `gpiozero` and `schedule`. If missing, installs `python3-pip` via `opkg` and fetches required PIP packages.
3. **GPIO Registration:** Adds Relay 2 (`2 out relay_2`) to `/etc/venus/gpio_list` if not already registered.
4. **Service Registration:** Symlinks `/data/etc/irrigator/service` to `/service/irrigator` so Venus OS `daemontools` automatically starts and monitors the process.
5. **Firmware Upgrade Persistence:** Adds `bash /data/etc/irrigator/install.sh` to `/data/rc.local`. Because Venus OS wipes `/` on firmware updates but preserves `/data`, `/data/rc.local` automatically re-installs the service and GPIO configs on the first boot after an OS update.

---

## ⚙️ Service Control Commands

Use standard `daemontools` commands or helper scripts to manage the service:

* **Check Service Status:**
  ```bash
  svstat /service/irrigator
  ```

* **Restart Service:**
  ```bash
  ./restart.sh
  # or: svc -t /service/irrigator
  ```

* **Stop Service:**
  ```bash
  svc -d /service/irrigator
  ```

* **Start Service:**
  ```bash
  svc -u /service/irrigator
  ```

* **View Logs:**
  ```bash
  tail -f /var/log/irrigator/current
  ```

* **Uninstall Service:**
  ```bash
  bash uninstall.sh
  ```

---

## 📄 License

MIT License.
