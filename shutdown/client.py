
import time
import sys
import socket
import os

host = socket.gethostname()
port = 8000

s = socket.socket()
s.connect((host, port))

print ("Connected to server")


command = s.recv(16)
command = command.decode('utf-8')

if command == 'shutdown':
    print ("")
    print ("shutdown command")
    s.send("Command recieved!".encode('utf-8'))
    os.system("shutdown.bat")