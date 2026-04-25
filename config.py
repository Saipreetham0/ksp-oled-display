# ─────────────────────────────────────────────
#  KSP Electronics — Shared Configuration
# ─────────────────────────────────────────────

# ── OLED Display ─────────────────────────────
OLED_WIDTH        = 128       # pixels
OLED_HEIGHT       = 64        # pixels
OLED_I2C_ADDR     = 0x3C      # default SSD1306 address (try 0x3D if not found)
BOOT_LOGO_SECONDS = 4         # how long to show the KSP boot logo
STATS_REFRESH_SEC = 1         # stats screen refresh interval (seconds)
TEMP_BAR_MAX_C    = 85        # temperature that fills the bar to 100%

# ── Fonts ─────────────────────────────────────
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

FONT_SIZE_KSP   = 38   # large "KSP" on boot logo
FONT_SIZE_ELEC  = 13   # "ELECTRONICS" on boot logo
FONT_SIZE_LABEL = 10   # stat row labels
FONT_SIZE_VALUE = 10   # stat row values

# ── PWM Fan Control ───────────────────────────
FAN_GPIO_PIN      = 14    # BCM pin connected to fan PWM signal
FAN_PWM_FREQ      = 100   # PWM frequency in Hz
FAN_ON_TEMP_C     = 40    # fan turns on at this CPU temperature (°C)
FAN_POLL_SEC      = 1     # how often to check temperature (seconds)
