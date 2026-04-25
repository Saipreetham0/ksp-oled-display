import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.OUT)
pwm = GPIO.PWM(14, 100)

print("\nPress Ctrl+C to quit \n")
dc = 0
pwm.start(dc)

try:
    while True:
        temp = subprocess.getoutput("vcgencmd measure_temp|sed 's/[^0-9.]//g'")
        print(f"Current CPU Temperature is: {temp} degree")
        if round(float(temp)) >= 40:
            dc = 100
            pwm.ChangeDutyCycle(dc)
        else:
            dc = 0
            pwm.ChangeDutyCycle(dc)
        time.sleep(1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
    print("Ctrl + C pressed -- Ending program")
