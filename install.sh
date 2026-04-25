#!/bin/bash
# KSP Electronics — One-shot installer (OLED + PWM Fan Control)

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Installing from: $REPO_DIR"

echo "==> Enabling I2C..."
sudo raspi-config nonint do_i2c 0

echo "==> Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y i2c-tools python3-dev libfreetype6-dev libjpeg-dev

echo "==> Installing Python libraries..."
pip3 install -r "$REPO_DIR/requirements.txt" --break-system-packages

echo "==> Verifying OLED on I2C bus 1..."
i2cdetect -y 1

echo "==> Patching service files with repo path..."
sed -i "s|/home/pi/ksp-oled-display|$REPO_DIR|g" "$REPO_DIR/ksp-oled.service"
sed -i "s|/home/pi/ksp-oled-display|$REPO_DIR|g" "$REPO_DIR/pwm-fan-control.service"

echo "==> Installing systemd services..."
sudo cp "$REPO_DIR/ksp-oled.service"        /etc/systemd/system/ksp-oled.service
sudo cp "$REPO_DIR/pwm-fan-control.service" /etc/systemd/system/pwm-fan-control.service

sudo systemctl daemon-reload

sudo systemctl enable ksp-oled.service
sudo systemctl start  ksp-oled.service

sudo systemctl enable pwm-fan-control.service
sudo systemctl start  pwm-fan-control.service

echo ""
echo "Done!"
echo "Check OLED status:  sudo systemctl status ksp-oled"
echo "Check fan status:   sudo systemctl status pwm-fan-control"
