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

connection, address = server_socket.accept()
# data, addr = server_socket.recv(512) # random buffer size, doesn't matter here..
print("Beginning client communication: ")

server_socket.sendall(b'Server communication established')
while connection:
    for i in range(6):
        # axis[i], addr = connection.recv(512)
        axis[i] = connection.recv(512)
    for i in range(16):
        # button[i], addr = connection.recv(512)
        button[i] = connection.recv(512)
    print(axis)
    print(button)
