import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# Initialize BCM pin 18 as output
GPIO.setup(18, GPIO.OUT)

while True:

    #This Turns Relay On.
    GPIO.output(18, 1)
    sleep(1)
    # Turns Relay Off.
    GPIO.output(18, 0)
    sleep(1)
