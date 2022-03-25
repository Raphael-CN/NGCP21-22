import serial
import math
from time import sleep
import numpy as np
import struct

ser0 = serial.Serial("/dev/ttyS0", 115200,
                     parity = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout=1)
ser1 = serial.Serial("/dev/ttyAMA2", 115200,
                     parity = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout = 1)
ser2 = serial.Serial("/dev/ttyAMA3", 115200,
                     parity = serial.PARITY_NONE,
                     stopbits = serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     timeout = 1)

class Uart():
    def write(self, ser, input):
        ser.write(bytes(str(input), 'utf-8'))

    def read_int(self, ser, num):
        serialdata = ser.read(num)
        ser.write(bytes(str(count), 'utf-8'))
        if serialdata >= bytes(str(0), 'utf-8') and serialdata <= bytes(str(9),'utf-8'):
            serialdata = int(serialdata.decode('utf-8'))
        else:
            serialdata0 = 0
        return serialdata0

    def readline(self, ser):
        serialdata = ser.readline()[:-2]
        return serialdata

class GPS():
    def dms_to_dd(self, degrees, minutes, seconds):
        dd = degrees+ (minutes/60)+ (seconds/3600)
        return dd
    
    def findBearing(self, latStart, longStart, latEnd, longEnd):
        '''
        Returns the angle and distance between bot and hiker location
        '''
        #uses the haversine function in order to find the great-circle distance between 2 points
        #reference: https://www.movable-type.co.uk/scripts/latlong.html
        dLat = (latEnd - latStart) * math.pi / 180.0
        dLon = (longEnd - longStart) * math.pi / 180.0
        latStart = latStart * math.pi / 180.0
        latEnd = latEnd * math.pi / 180.0

        y = math.sin(dLon) * math.cos(latEnd)
        x = math.cos(latStart) * math.sin(latEnd) - math.sin(latStart) * math.cos(latEnd) * math.cos(dLon)
        bearing_rad = math.atan2(y, x)
        bearing_deg = (bearing_rad*180/math.pi + 360) % 360
        return bearing_deg
    
    def bytes_to_DMS(self, GPS_input):
        hex_to_ascii = GPS_input.fromhex(GPS_input.decode("ascii"))
        ascii_to_string = ''.join(chr(i) for i in hex_to_ascii)
        degrees = int(ascii_to_string.split('°')[0])
        minutes = int((ascii_to_string.split("'")[0]).split("°")[1])
        seconds = float((ascii_to_string.split("'")[1]).split('"')[0])
        return degrees, minutes, seconds

count = 0
init = 0
while True:
    if init == 0:
        serialdata0 = Uart.readline(ser0)
        serialdata1 = Uart.readline(ser1)
        serialdata2 = Uart.readline(ser2)
        print(serialdata0)
        print(serialdata1)
        print(serialdata2)
        print()
        #serialdata3 = ser3.readline()[:-2]
        #print(serialdata3)
        #serialdata0 = ser0.readline()[:-2]
    #if serialdata0 != b'':
        #serialdata0 = int(serialdata0.decode('utf-8'))
        #ser0.write(bytes(str(count), 'utf-8'))
        #print(serialdata0)
        #if serialdata0 != b'':
        #    print(bytes.hex(serialdata0))
        #    ser0.reset_output_buffer()
            #init = 1
    #if init == 1:
        #ser0.write(serialdata0)
        #init = 0
    #count = count + 1
    #sleep(0.2)
    #print("Hi")


