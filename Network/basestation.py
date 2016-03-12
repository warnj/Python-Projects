# this sends commands over the network to a recieving computer

# this recieves a potentiometer value from an arduino connected to this computer and sends that
# to a recieving computer that should send that value to an arduino (and a servo) connected to that computer

import serial
import socket

UDP_IP = "173.250.189.211"  # 90% sure this should be the target ip
UDP_PORT = 8888

salmon = serial.Serial("COM3", 9600)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    potPos = salmon.readline()
    print (potPos)
    sock.sendto(str(potPos), (UDP_IP, UDP_PORT))


