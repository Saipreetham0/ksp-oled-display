# KSP Electronics — Raspberry Pi 4B OLED Display

A Python project for driving a **0.96" SSD1306 OLED display** (128×64, I2C) on a Raspberry Pi 4B.  
Shows a **KSP Electronics boot logo** followed by a **live system stats dashboard** — IP address, CPU load, RAM usage, and Disk usage — updating every second.  
Runs automatically on boot via a **systemd service**.

---

## Preview

### Boot Logo
```
┌─────────────────────────────┐
│  ┌───────────────────────┐  │
│  │   KSP  (large, bold)  │  │  ← White block, black letters
│  └───────────────────────┘  │
│        ELECTRONICS           │
│        ───────────           │
└─────────────────────────────┘
```

### Live Stats Screen
```
┌──── KSP ELECTRONICS ────────┐  ← Inverted header
│ IP:  192.168.1.x            │
│ CPU:  12.5%  [████░░░░░░░] │
│ MEM:  45.2%  [███████░░░░] │
│ DSK:  18.9%  [███░░░░░░░░] │
└─────────────────────────────┘
```

---

## Hardware

| Component | Details |
|-----------|---------|
| Board | Raspberry Pi 4B |
| Display | 0.96" OLED — SSD1306, 128×64, I2C |
| I2C Address | `0x3C` (default) |

### Wiring

| OLED Pin | Raspberry Pi 4B Pin | GPIO |
|----------|---------------------|------|
| VCC      | Pin 1               | 3.3V |
| GND      | Pin 6               | GND  |
| SDA      | Pin 3               | GPIO 2 |
| SCL      | Pin 5               | GPIO 3 |

---

## Requirements

- Raspberry Pi 4B running Raspberry Pi OS (Bookworm or newer)
- Python 3.11+
- I2C enabled

### Python Libraries

```
adafruit-blinka
adafruit-circuitpython-ssd1306
pillow
psutil
```

---

## Installation

### Option 1 — One-shot installer (recommended)

```bash
git clone https://github.com/KSP-ELECTRONICS/ksp-oled-display.git
cd ksp-oled-display
chmod +x install.sh
./install.sh
```

### Option 2 — Manual steps

**1. Enable I2C**
```bash
sudo raspi-config nonint do_i2c 0
```

**2. Install system packages**
```bash
sudo apt-get install -y i2c-tools python3-dev libfreetype6-dev libjpeg-dev
```

**3. Install Python libraries**
```bash
pip3 install -r requirements.txt --break-system-packages
```

**4. Verify OLED is detected**
```bash
i2cdetect -y 1
# Should show 0x3C on the grid
```

**5. Run manually**
```bash
python3 ksp_oled.py
```

**6. Install as a service (auto-start on boot)**
```bash
sudo cp ksp-oled.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ksp-oled
sudo systemctl start ksp-oled
```

---

## Service Management

| Action | Command |
|--------|---------|
| Check status | `sudo systemctl status ksp-oled` |
| Stop | `sudo systemctl stop ksp-oled` |
| Restart | `sudo systemctl restart ksp-oled` |
| View live logs | `sudo journalctl -u ksp-oled -f` |
| Disable autostart | `sudo systemctl disable ksp-oled` |

---

## File Structure

```
ksp-oled-display/
├── ksp_oled.py          # Main display script
├── ksp-oled.service     # systemd service unit
├── install.sh           # One-shot installer
├── requirements.txt     # Python dependencies
└── README.md
```

---

## How It Works

1. **Boot logo** — On startup, renders `KSP` in a large inverted (white-block/black-text) style with `ELECTRONICS` underneath. Displayed for 4 seconds.
2. **Stats loop** — Switches to a live dashboard with:
   - **IP** — primary network IP via `hostname -I`
   - **CPU** — load percentage via `psutil`
   - **MEM** — RAM usage percentage + progress bar
   - **DSK** — Root disk usage percentage + progress bar
   - Refreshes every second

---

## License

MIT License — free to use, modify, and distribute.

---

*Made with ❤️ by KSP Electronics*
