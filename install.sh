#!/bin/bash
# KSP Electronics OLED Display — One-shot installer

set -e

echo "==> Enabling I2C..."
sudo raspi-config nonint do_i2c 0

echo "==> Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y i2c-tools python3-dev libfreetype6-dev libjpeg-dev

echo "==> Installing Python libraries..."
pip3 install -r requirements.txt --break-system-packages

echo "==> Verifying OLED on I2C bus 1..."
i2cdetect -y 1

echo "==> Installing systemd service..."
sudo cp ksp-oled.service /etc/systemd/system/ksp-oled.service
sudo systemctl daemon-reload
sudo systemctl enable ksp-oled.service
sudo systemctl start ksp-oled.service

echo ""
echo "Done! KSP Electronics OLED display is running."
echo "Check status: sudo systemctl status ksp-oled"
