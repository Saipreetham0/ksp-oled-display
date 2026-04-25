#!/usr/bin/env python3
"""
KSP Electronics OLED Display
Boot logo + live system stats (IP, CPU, Temp, RAM, Disk)
"""
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import psutil
import time
import subprocess

from config import (
    OLED_WIDTH, OLED_HEIGHT, OLED_I2C_ADDR,
    BOOT_LOGO_SECONDS, STATS_REFRESH_SEC, TEMP_BAR_MAX_C,
    FONT_BOLD, FONT_MONO,
    FONT_SIZE_KSP, FONT_SIZE_ELEC, FONT_SIZE_LABEL, FONT_SIZE_VALUE,
)

# ── Display setup ─────────────────────────────────────────────────
i2c  = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_I2C_ADDR)
oled.fill(0)
oled.show()

# ── Fonts ─────────────────────────────────────────────────────────
f_ksp   = ImageFont.truetype(FONT_BOLD, FONT_SIZE_KSP)
f_elec  = ImageFont.truetype(FONT_BOLD, FONT_SIZE_ELEC)
f_label = ImageFont.truetype(FONT_BOLD, FONT_SIZE_LABEL)
f_value = ImageFont.truetype(FONT_MONO, FONT_SIZE_VALUE)

# ── Helpers ───────────────────────────────────────────────────────
def text_w(draw, text, font):
    return draw.textlength(text, font=font)

def get_ip():
    try:
        out = subprocess.check_output(["hostname", "-I"], text=True).strip()
        return out.split()[0] if out else "No IP"
    except Exception:
        return "No IP"

def get_cpu():
    return psutil.cpu_percent(interval=0.5)

def get_mem():
    m = psutil.virtual_memory()
    return m.percent, m.used // (1024**2), m.total // (1024**2)

def get_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0
    except Exception:
        try:
            t = psutil.sensors_temperatures()
            return list(t.values())[0][0].current
        except Exception:
            return 0.0

def get_disk():
    d = psutil.disk_usage("/")
    return d.percent, d.used // (1024**3), d.total // (1024**3)

def draw_bar(draw, x, y, w, h, pct, fill=1):
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=fill, fill=0)
    filled = int((pct / 100) * (w - 2))
    if filled > 0:
        draw.rectangle([x + 1, y + 1, x + filled, y + h - 2], fill=fill)

def show(img):
    oled.image(img)
    oled.show()

# ══════════════════════════════════════════════════════════════════
# BOOT LOGO
# ══════════════════════════════════════════════════════════════════
img  = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), 0)
draw = ImageDraw.Draw(img)

ksp_text = "KSP"
kw = int(text_w(draw, ksp_text, f_ksp))
kh = 42
kx = (OLED_WIDTH - kw) // 2 - 4
ky = 2
draw.rectangle([kx - 2, ky, kx + kw + 5, ky + kh], fill=1)
draw.text((kx + 1, ky - 1), ksp_text, font=f_ksp, fill=0)

e_text = "ELECTRONICS"
ew = int(text_w(draw, e_text, f_elec))
ex = (OLED_WIDTH - ew) // 2
ey = ky + kh + 3
draw.text((ex, ey), e_text, font=f_elec, fill=1)
draw.line([ex, ey + 14, ex + ew, ey + 14], fill=1)

show(img)
time.sleep(BOOT_LOGO_SECONDS)

# ══════════════════════════════════════════════════════════════════
# STATS LOOP
# ══════════════════════════════════════════════════════════════════
while True:
    img  = Image.new("1", (OLED_WIDTH, OLED_HEIGHT), 0)
    draw = ImageDraw.Draw(img)

    ip      = get_ip()
    cpu_pct = get_cpu()
    temp_c  = get_temp()
    mem_pct, mem_used, mem_tot = get_mem()
    dsk_pct, dsk_used, dsk_tot = get_disk()

    # Header
    draw.rectangle([0, 0, OLED_WIDTH - 1, 11], fill=1)
    hdr = "KSP ELECTRONICS"
    hw  = int(text_w(draw, hdr, f_label))
    draw.text(((OLED_WIDTH - hw) // 2, 1), hdr, font=f_label, fill=0)

    rows = [13, 23, 33, 43, 53]
    BAR_X, BAR_W, BAR_H = 68, 57, 6

    y = rows[0]
    draw.text((0, y), "IP:", font=f_label, fill=1)
    draw.text((18, y), ip, font=f_value, fill=1)

    y = rows[1]
    draw.text((0, y), "CPU:", font=f_label, fill=1)
    draw.text((27, y), f"{cpu_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 2, BAR_W, BAR_H, cpu_pct)

    y = rows[2]
    draw.text((0, y), "TMP:", font=f_label, fill=1)
    draw.text((27, y), f"{temp_c:5.1f}°C", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 2, BAR_W, BAR_H, min(temp_c / TEMP_BAR_MAX_C * 100, 100))

    y = rows[3]
    draw.text((0, y), "MEM:", font=f_label, fill=1)
    draw.text((27, y), f"{mem_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 2, BAR_W, BAR_H, mem_pct)

    y = rows[4]
    draw.text((0, y), "DSK:", font=f_label, fill=1)
    draw.text((27, y), f"{dsk_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 2, BAR_W, BAR_H, dsk_pct)

    show(img)
    time.sleep(STATS_REFRESH_SEC)
