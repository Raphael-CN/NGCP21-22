from gpiozero import Motor

motor = Motor(27, 18, enable = 25)
motor.forward()
