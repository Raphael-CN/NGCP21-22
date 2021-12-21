import pigpio  # Import the pigpio library for easy PWM Functionality
from threading import Timer

# TODO: Need substitute to TimerOne

### Globals for Motor 1 and its encoder ###
### Constants are all capitalized in Python ###

M1ENCA = 18 # GPIO Pin 18 (PWM0) in BCM
M1ENCB = 13 # GPIO Pin 13 (PWM1) in BCM
M1CW = 23 # IN1 pin
M1CCW = 24 # IN2 pin
M1CPR = 64

M1Anow = 0
M1Bnow = 0
M1Apast = 0
M1Bpast = 0
M1encCount = 0

#### End of Motor 1 and its encoder variables ###

### Globals for PID ###

kp = 1
ki = 1
kd = 0
setRPM = 750.0
calcRPM = 0.0
M1PWM = 0
M1PWR = 9
err = 0
pastErr = 0
errSum = 0
dErr = 0

# Initialize GPIO pins in BCM Mode

pi = pigpio.pi()

pi.set_mode(M1ENCA, GPIO.IN)
pi.set_mode(M1ENCB, GPIO.IN)

pi.set_mode(M1CW, GPIO.OUT)
pi.set_mode(M1CCW, GPIO.OUT)

### Interrupt Service Routines ###

# M1ENC() used to write present and past values Motor1's encoder channels

def M1ENC():
    global M1Anow, M1Bnow 
    M1Anow = pi.get_PWM_frequency(M1ENCA)
    M1Bnow = pi.get_PWM_frequency(M1ENCB)

    global M1encCount
    M1encCount += ParseEncoder()

    global M1Apast, M1Bpast
    M1Apast = M1Anow
    M1Bpast = M1Bnow

def ParseEncoder():

    if M1Apast and M1Bpast:
        if M1Anow and (not M1Bnow):
            return 1
        if (not M1Anow) and M1Bnow:
            return -1
    elif (not M1Apast) and M1Bpast:
        if M1Anow and M1Bnow:
            return 1
        if (not M1Anow) and (not M1Bnow):
            return -1
    elif (not M1Apast) and (not M1Bpast):
        if (not M1Anow) and M1Bnow:
            return 1
        if M1Anow and (not M1Bnow):
            return -1
    elif M1Apast and (not M1Bpast):
        if (not M1Anow) and (not M1Bnow):
            return 1
        if M1Anow and M1Bnow:
            return -1

def ISR_timerone():
    # TODO: Need substitute to TimerOne

    #Timer1.detachInterrupt();  # Stop the timer

    global M1PWM

    print("Set RPM: ")
    print(setRPM)
    print(" RPM -")

    print("  Motor1 PWM: ")
    print(M1PWM)

    print("- Encoder Ticks: ")
    print(M1encCount)

    print("  Motor1 Speed : ")
    # calculate RPM for Motor 1 = [(num. of counts in 1 sec)/(counts in 1 revolution)]x(60 seconds in 1 min.)
    global calcRPM 
    calcRPM = (M1encCount / M1CPR) * 60.00
    # Counts per Rotation = 4 x PPR
    print(calcRPM)
    print(" RPM - ")
    global M1encCount
    M1encCount = 0  #  reset counter to zero

    print("  Error : ")
    if calcRPM < setRPM:
        err = 1
    elif calcRPM > setRPM:
        err = -1
    else:
        err = 0

    print(err)

    print(" Error Sum: ")
    global errSum, pastErr
    errSum += (ki * pastErr)
    pastErr = err
    print(errSum)
    print("\n")

    if setRPM > 0:
        pi.write(M1CW, 1)
        pi.write(M1CCW, 0)

    elif setRPM < 0:
        pi.write(M1CW, 0)
        pi.write(M1CCW, 1)

    elif setRPM == 0:
        pi.write(M1CW, 0)
        pi.write(M1CCW, 0)

    M1PWM = (kp * err) + errSum

    # Timer1.setPwmDuty(M1PWR, M1PWM)
    pi.set_PWM_dutycycle(M1PWR, M1PWM)

    #Timer1.attachInterrupt(ISR_timerone)  # Enable the timer

def setup():

    # TODO: Need substitute to TimerOne

    # Timer1.initialize(500000) # set timer for 1sec
    pi.set_PWM_dutycycle(M1PWR, 0)
    # Timer1.pwm(M1PWR, 0)

    # Increase counter 1 when speed sensor pin goes changes H/L->L/H
    pi.callback(M1ENCA, pigpio.EITHER_EDGE, M1ENC)
    # attachInterrupt(digitalPinToInterrupt (M1encA), M1ENC, CHANGE)

    # Increase counter 2 when speed sensor pin goes changes H/L->L/H
    pi.callback(M1ENCB, pigpio.EITHER_EDGE, M1ENC)
    # attachInterrupt(digitalPinToInterrupt (M1encB), M1ENC, CHANGE)

    # Enable the timer
    # Timer1.attachInterrupt(ISR_timerone())

if __name__ == '__main__':
    setup()
    # Put your main code here, to run repeatedly
    getRPM = Timer(1.0, ISR_timerone())
    getRPM.start()