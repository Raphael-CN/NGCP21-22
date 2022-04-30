# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_bno055_header
import csv
import math

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055_header.BNO055_I2C(i2c)

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

#time.sleep(3)
initialLoop = True
initialHeading = 0
loop_count = 100
i = 0

print(sensor.calibration_status)
calibration_status = bool
sensor.set_calibration([0, 0, 0, 0, 0, 0,         # offset accelerometer
                        176, 0, 85, 0, 232, 254,  # offset magnetometer
                        252, 255, 251, 255, 1, 0, # offset gyroscope
                        232, 0,
                        0, 0])
print(sensor.offsets_magnetometer)
time.sleep(1)
while True:
    #gyroRounded = [round(num, 4) for num in sensor.gyro]
    #gyroDegree = [round(num * 180/math.pi, 4) for num in sensor.gyro]
    #print("Quaternion: {}".format(sensor.quaternion))
    #orientation = [num for num in sensor.magnetic]
    #print("Temperature: {} degrees C" .format(sensor.temperature))
    #print("Temperature: {} degrees F" .format(sensor.temperature*9/5+32))
    """
    print(
        "Temperature: {} degrees C".format(temperature())
    )  # Uncomment if using a Raspberry Pi
    """
    print()
    print("Euler angle: " + str(sensor.euler[0]))
    #print("Accelerometer* (m/s^2): " +str(sensor.acceleration))
    #print("Magnetometer (microteslas): " + str(sensor.magnetic))
    #print("Magnetometer (microteslas): " + str(orientation))
    #print("Gyroscope* (deg/sec): " + str(sensor.gyro[0] * 180/math.pi) + " " + str(sensor.gyro[1] * 180/math.pi) + " " + str(sensor.gyro[2] * 180/math.pi))
    #print("Gyro (rad/sec): " + str(gyroRounded))
    #print("Euler angle: " + str(sensor.euler))
    #print("Linear acceleration* (m/s^2): " + str(sensor.linear_acceleration))
    #print("Gravity (m/s^2): " + str(sensor.gravity))
    #print(sensor.acceleration)
    
    print("Compass: " + str(180 + math.atan2(sensor.magnetic[1], sensor.magnetic[0]) * 180 / math.pi))
    #print("Gyroscope* (deg/sec): " + str(gyroDegree))
    #t = time.localtime()
    #current_time = time.strftime("%H:%M:%S", t)
    #print(current_time)
    #with open('IMU_values.csv','a',newline='') as file:
        #mywriter = csv.writer(file,delimiter=',')
        #file.write("Time: " + str(current_time) + "\n\r")
        #file.write("Accelerometer* (m/s^2): " + str(sensor.acceleration) + "\n\r")
        #file.write("Gravity (m/s^2): " + str(sensor.gravity) + "\n\r")
    time.sleep(0.01)
#     
#     while initialLoop == True:
#         if sensor.calibration_status[3] == 3:
#             while i < loop_count:
#                 sensor_euler_0 = sensor.euler[0]
#                 if sensor_euler_0 is not None:
#                     if sensor_euler_0 < 1 or sensor_euler_0 > 359:
#                         initialHeading+=abs(180+math.atan2(sensor.magnetic[1], sensor.magnetic[0])*180/math.pi)
#                         i += 1
#                         if i == loop_count:
#                             initialLoop = False
#                             initialHeading = initialHeading/i
#                         print(str(i)+" Initial Heading: " + str(initialHeading))
#                         time.sleep(0.01)
#                     else:
#                         print("Euler: " + str(sensor_euler_0))
#                         print("Compass: " + str(180 + math.atan2(sensor.magnetic[1], sensor.magnetic[0]) * 180 / math.pi))
#                         print("Please position IMU so euler is around 0: Press enter when ready")
#                         input()
#                         sensor_euler_0 = sensor.euler[0]
#                         
#         else:
#             print(sensor.calibration_status[3])
#             print("Please calibrate IMU: press enter when ready")
#             input()
#     sensor_euler_0 = sensor.euler[0]
#     if sensor_euler_0 is not None:
#         print("Euler angle: " + str((sensor_euler_0 + initialHeading) % 360))
#         print("Compass: " + str(180 + math.atan2(sensor.magnetic[1], sensor.magnetic[0]) * 180 / math.pi))
#         print(sensor.calibration_status[3])
#     time.sleep(0.01)
