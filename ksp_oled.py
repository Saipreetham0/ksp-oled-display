#!/usr/bin/env python3
"""
KSP Electronics OLED Display
Boot logo + live system stats (IP, CPU, RAM, Disk)
128x64 SSD1306 I2C at 0x3C
"""
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import psutil
import time
import subprocess

# ── Display setup ────────────────────────────────────────────────
WIDTH, HEIGHT, ADDR = 128, 64, 0x3C
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=ADDR)
oled.fill(0)
oled.show()

# ── Fonts ────────────────────────────────────────────────────────
BOLD  = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG   = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

f_ksp   = ImageFont.truetype(BOLD, 38)   # "KSP" — large & bold
f_elec  = ImageFont.truetype(BOLD, 13)   # "ELECTRONICS"
f_label = ImageFont.truetype(BOLD, 10)   # stat labels
f_value = ImageFont.truetype(MONO, 10)   # stat values

# ── Helpers ──────────────────────────────────────────────────────
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

def get_disk():
    d = psutil.disk_usage("/")
    return d.percent, d.used // (1024**3), d.total // (1024**3)

def draw_bar(draw, x, y, w, h, pct, fill=1):
    """Draw a thin progress bar."""
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=fill, fill=0)
    filled = int((pct / 100) * (w - 2))
    if filled > 0:
        draw.rectangle([x + 1, y + 1, x + filled, y + h - 2], fill=fill)

def show(img):
    oled.image(img)
    oled.show()

# ════════════════════════════════════════════════════════════════
# BOOT LOGO — "KSP" big & inverted, "ELECTRONICS" below
# ════════════════════════════════════════════════════════════════
img = Image.new("1", (WIDTH, HEIGHT), 0)
draw = ImageDraw.Draw(img)

# --- KSP block (inverted = white box, black letters) ---
ksp_text = "KSP"
kw = int(text_w(draw, ksp_text, f_ksp))
kh = 42                           # block height
kx = (WIDTH - kw) // 2 - 4       # center with padding
ky = 2
draw.rectangle([kx - 2, ky, kx + kw + 5, ky + kh], fill=1)   # white bg
draw.text((kx + 1, ky - 1), ksp_text, font=f_ksp, fill=0)     # black text

# --- ELECTRONICS below ---
e_text = "ELECTRONICS"
ew = int(text_w(draw, e_text, f_elec))
ex = (WIDTH - ew) // 2
ey = ky + kh + 3
draw.text((ex, ey), e_text, font=f_elec, fill=1)

# thin underline
draw.line([ex, ey + 14, ex + ew, ey + 14], fill=1)

show(img)
time.sleep(4)   # hold boot logo 4 seconds

# ════════════════════════════════════════════════════════════════
# STATS LOOP — IP / CPU / MEM / DISK, refreshes every second
# ════════════════════════════════════════════════════════════════
while True:
    img = Image.new("1", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(img)

    ip      = get_ip()
    cpu_pct = get_cpu()
    mem_pct, mem_used, mem_tot = get_mem()
    dsk_pct, dsk_used, dsk_tot = get_disk()

    # ── Header bar ──────────────────────────────────────────────
    draw.rectangle([0, 0, WIDTH - 1, 12], fill=1)
    hdr = "KSP ELECTRONICS"
    hw = int(text_w(draw, hdr, f_label))
    draw.text(((WIDTH - hw) // 2, 1), hdr, font=f_label, fill=0)

    # ── Layout: 4 rows below header ─────────────────────────────
    # Row positions
    rows = [15, 27, 39, 51]
    BAR_X, BAR_W, BAR_H = 68, 57, 6

    # ── IP ──────────────────────────────────────────────────────
    y = rows[0]
    draw.text((0, y), "IP:", font=f_label, fill=1)
    draw.text((18, y), ip, font=f_value, fill=1)

    # ── CPU ─────────────────────────────────────────────────────
    y = rows[1]
    draw.text((0, y), "CPU:", font=f_label, fill=1)
    draw.text((27, y), f"{cpu_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 1, BAR_W, BAR_H, cpu_pct)

    # ── Memory ──────────────────────────────────────────────────
    y = rows[2]
    draw.text((0, y), "MEM:", font=f_label, fill=1)
    draw.text((27, y), f"{mem_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 1, BAR_W, BAR_H, mem_pct)

    # ── Disk ────────────────────────────────────────────────────
    y = rows[3]
    draw.text((0, y), "DSK:", font=f_label, fill=1)
    draw.text((27, y), f"{dsk_pct:5.1f}%", font=f_value, fill=1)
    draw_bar(draw, BAR_X, y + 1, BAR_W, BAR_H, dsk_pct)

    show(img)
    time.sleep(1)
