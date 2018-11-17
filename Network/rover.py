# This recieves commands from a network connection and prints the data recieved

# the commented out lines of code will send the recieved commands to an arduino over serial

import serial
import socket

UDP_IP = '173.250.159.234' # my own v4  IP address -
# type ip address into google or ipconfig into cmd.exe to get this number - may need to add this value to sending code
UDP_PORT = 8888

#ser = serial.Serial("COM3", 9600)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print("received message:", data)
    # ser.write(data)
    # ser.write('\n')


