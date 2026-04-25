import RPi.GPIO as GPIO
import time
import subprocess

from config import FAN_GPIO_PIN, FAN_PWM_FREQ, FAN_ON_TEMP_C, FAN_POLL_SEC

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_GPIO_PIN, GPIO.OUT)
pwm = GPIO.PWM(FAN_GPIO_PIN, FAN_PWM_FREQ)

print("\nPress Ctrl+C to quit \n")
dc = 0
pwm.start(dc)

try:
    while True:
        temp = subprocess.getoutput("vcgencmd measure_temp|sed 's/[^0-9.]//g'")
        print(f"Current CPU Temperature is: {temp} degree")
        if round(float(temp)) >= FAN_ON_TEMP_C:
            dc = 100
            pwm.ChangeDutyCycle(dc)
        else:
            dc = 0
            pwm.ChangeDutyCycle(dc)
        time.sleep(FAN_POLL_SEC)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Ctrl + C pressed -- Ending program")
