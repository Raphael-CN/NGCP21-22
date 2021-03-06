import pigpio

pi = pigpio.pi()

solenoidENA = 13 #pin number (BCM) for ENA input on driver
solenoidIn1 = 6 #pin number (BCM) for In1 input on driver
solenoidIn2 = 5 #pin number (BCM) for In2 input on driver

pi.set_mode(solenoidENA, pigpio.OUTPUT)
pi.set_mode(solenoidIn1, pigpio.OUTPUT)
pi.set_mode(solenoidIn2, pigpio.OUTPUT)

pi.write(solenoidIn1, 0)
pi.write(solenoidIn2, 1)

while True:
  pi.set_PWM_dutycycle(solenoidENA, 64)
  pi.set_PWM_dutycycle(solenoidENA, 0)

