import socket
import numpy as np
import sys
from struct import *
import base64

TCP_IP = "192.168.1.95" # listen to everything
TCP_PORT = 12345 # port

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen()

# Define variables
axis = np.zeros(6)
button = np.zeros(16)

data, addr = server_socket.recvfrom(512) # random buffer size, doesn't matter here..
print("Beginning client communication: ")

server_socket.sendto(b'Server communication established', addr)
while True:
    for i in range(6):
        axis[i], addr = server_socket.recvfrom(512)
    for i in range(16):
        button[i], addr = server_socket.recvfrom(512)
    print(axis)
    print(button)
