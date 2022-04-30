# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bno055
import math

# wire connection from raspberry PI 4 to BNO055 is using I2C 
i2c = board.I2C()
sensor = adafruit_bno055.BNO055_I2C(i2c, address = 40)

# default mode with all the sensors turned on.
sensor.mode = adafruit_bno055.NDOF_MODE


# If you are going to use UART uncomment these lines
# uart = board.UART()
# sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF


def temperature():
    global last_val  # pylint: disable=global-statement
    result = sensor.temperature
    if abs(result - last_val) == 128:
        result = sensor.temperature
        if abs(result - last_val) == 128:
            return 0b00111111 & result
    last_val = result
    return result

while True:
  

    gyroRounded = [round(num, 4) for num in sensor.gyro]
    orientation = [num for num in sensor.magnetic]
    
    print("Heading:" + str(sensor.euler[0]) + "°")
    print("Temperature: {} degrees C" .format(sensor.temperature))
    print("Temperature: {} degrees F" .format(sensor.temperature*9/5+32))
    print("Accelerometer* (m/s^2): " +str(sensor.acceleration))
    print("Magnetometer (microteslas): " + str(sensor.magnetic))
    print("Magnetometer (microteslas): " + str(orientation))
    print("Gyroscope* (rad/sec): " + str(sensor.gyro))
    print("Gyro (rad/sec): " + str(gyroRounded))
    print("Euler angle (degree): " + str(sensor.euler))
    print("Linear acceleration* (m/s^2): " + str(sensor.linear_acceleration))
    print("Gravity (m/s^2): " + str(sensor.gravity))
    print("Quaternion: {}".format(sensor.quaternion))

    time.sleep(0.1)
