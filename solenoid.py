import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# Initialize BCM pin 18 as output
GPIO.setup(13, GPIO.OUT)

while True:

    #This Turns Relay Off. Brings Voltage to Max GPIO can output ~3.3V
    GPIO.output(13, 1)
    sleep(1)
    # Turns Relay On. Brings Voltage to Min GPIO can output ~0V.
    GPIO.output(13, 0)
    sleep(1)
