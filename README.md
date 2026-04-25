# KSP Electronics — Raspberry Pi 4B OLED Display + PWM Fan Control

A Python project for driving a **0.96" SSD1306 OLED display** (128×64, I2C) on a Raspberry Pi 4B and automatically controlling a **PWM fan** based on CPU temperature.  
Shows a **KSP Electronics boot logo** followed by a **live system stats dashboard** — IP address, CPU load, CPU temperature, RAM usage, and Disk usage — updating every second.  
Both features run automatically on boot via **systemd services**.

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
│ TMP:  45.2°C [█████░░░░░░] │
│ MEM:  45.0%  [███████░░░░] │
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
| Fan | 5V PWM fan via GPIO 14 (Pin 8) |

### OLED Wiring

| OLED Pin | Raspberry Pi 4B Pin | GPIO |
|----------|---------------------|------|
| VCC      | Pin 1               | 3.3V |
| GND      | Pin 6               | GND  |
| SDA      | Pin 3               | GPIO 2 |
| SCL      | Pin 5               | GPIO 3 |

### Fan Wiring

| Fan Pin  | Raspberry Pi 4B Pin | GPIO |
|----------|---------------------|------|
| VCC      | 5V (Pin 4)          | —    |
| GND      | GND (Pin 6)         | —    |
| PWM      | Pin 8               | GPIO 14 |

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
RPi.GPIO
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

## OLED Service Management

| Action | Command |
|--------|---------|
| Check status | `sudo systemctl status ksp-oled` |
| Stop | `sudo systemctl stop ksp-oled` |
| Restart | `sudo systemctl restart ksp-oled` |
| View live logs | `sudo journalctl -u ksp-oled -f` |
| Disable autostart | `sudo systemctl disable ksp-oled` |

---

## Configuration

All settings for both the OLED display and the fan are in one file: **`config.py`**

| Setting | Default | Description |
|---------|---------|-------------|
| `OLED_WIDTH` | `128` | Display width in pixels |
| `OLED_HEIGHT` | `64` | Display height in pixels |
| `OLED_I2C_ADDR` | `0x3C` | I2C address (try `0x3D` if display not found) |
| `BOOT_LOGO_SECONDS` | `4` | How long to show the KSP boot logo |
| `STATS_REFRESH_SEC` | `1` | Stats screen refresh interval |
| `TEMP_BAR_MAX_C` | `85` | Temperature that fills the bar to 100% |
| `FAN_GPIO_PIN` | `14` | BCM GPIO pin for fan PWM signal |
| `FAN_PWM_FREQ` | `100` | PWM frequency in Hz |
| `FAN_ON_TEMP_C` | `40` | CPU temperature (°C) that turns the fan on |
| `FAN_POLL_SEC` | `1` | How often to check temperature |

Edit `config.py` before running `install.sh` to customise for your hardware.

---

## File Structure

```
ksp-oled-display/
├── config.py                # All settings — edit this first
├── ksp_oled.py              # OLED display script
├── ksp-oled.service         # systemd service — OLED
├── pwm-fan-control.py       # PWM fan control script
├── pwm-fan-control.service  # systemd service — fan
├── install.sh               # One-shot installer (installs both)
├── requirements.txt         # Python dependencies
└── README.md
```

---

## PWM Fan Control

The fan runs automatically based on CPU temperature using `RPi.GPIO` PWM on **GPIO 14**.

| CPU Temperature | Fan Speed |
|-----------------|-----------|
| Below 40°C      | Off (0%)  |
| 40°C and above  | 100%      |

### Service Management

| Action | Command |
|--------|---------|
| Check status | `sudo systemctl status pwm-fan-control` |
| Stop | `sudo systemctl stop pwm-fan-control` |
| Restart | `sudo systemctl restart pwm-fan-control` |
| View live logs | `sudo journalctl -u pwm-fan-control -f` |
| Disable autostart | `sudo systemctl disable pwm-fan-control` |

---

## How It Works

1. **Boot logo** — On startup, renders `KSP` in a large inverted (white-block/black-text) style with `ELECTRONICS` underneath. Displayed for 4 seconds.
2. **Stats loop** — Switches to a live dashboard with:
   - **IP** — primary network IP via `hostname -I`
   - **CPU** — load percentage via `psutil` + progress bar
   - **TMP** — CPU temperature from `/sys/class/thermal` + bar (0–85 °C scale)
   - **MEM** — RAM usage percentage + progress bar
   - **DSK** — root disk usage percentage + progress bar
   - Refreshes every second

---

## License

MIT License — free to use, modify, and distribute.

---

*Made with ❤️ by KSP Electronics*
