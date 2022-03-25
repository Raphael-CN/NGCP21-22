import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)

    PIN_TRIGGER_1 = 7
    PIN_ECHO_1 = 11

    PIN_TRIGGER_2 = 31
    PIN_ECHO_2 = 29

    GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
    GPIO.setup(PIN_ECHO_1, GPIO.IN)

    GPIO.setup(PIN_TRIGGER_2, GPIO.OUT)
    GPIO.setup(PIN_ECHO_2, GPIO.IN)

    GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
    GPIO.output(PIN_TRIGGER_2, GPIO.LOW)

    while True:

        GPIO.output(PIN_TRIGGER_1, GPIO.HIGH)
        GPIO.output(PIN_TRIGGER_2, GPIO.HIGH)

        time.sleep(0.00001)

        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)
        GPIO.output(PIN_TRIGGER_2, GPIO.LOW)

        while GPIO.input(PIN_ECHO_1)==0:
            pulse_start_time_1 = time.time()
        while GPIO.input(PIN_ECHO_1)==1:
            pulse_end_time_1 = time.time()

        while GPIO.input(PIN_ECHO_2)==0:
            pulse_start_time_2 = time.time()
        while GPIO.input(PIN_ECHO_2)==1:
            pulse_end_time_2 = time.time()

        pulse_duration_1 = pulse_end_time_1 - pulse_start_time_1
        distance = round(pulse_duration_1 * 17150, 2)
        inches = round(distance * .393701, 2)
        print ("Distance:",distance,"cm ", "Inches:", inches)

        pulse_duration_2 = pulse_end_time_2 - pulse_start_time_2
        distance2 = round(pulse_duration_2 * 17150, 2)
        inches2 = round(distance2 * .393701, 2)
        print ("Distance:",distance2,"cm ", "Inches:", inches2)

        time.sleep(.5)
except KeyboardInterrupt:
    print("Measurements stopped.")
finally:
    GPIO.cleanup()
