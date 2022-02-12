import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# Initialize BCM pin 18 as output
GPIO.setup(18, GPIO.OUT)
solenoid = GPIO.PWM(18, 10)

solenoid.start(100)
input('Press return to stop:')   
solenoid.stop()
GPIO.cleanup()
