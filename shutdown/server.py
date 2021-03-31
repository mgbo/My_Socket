
import time
import sys
import socket
import os

s = socket.socket()
host = socket.gethostname()
port = 8000
s.bind((host, port))

print ("")
print ("Waiting for any incomming connections....")
print("")

s.listen(1)
conn, addr = s.accept()
print (addr, " - Has connnected to the server!")


command = input(str("Command : "))
print (command)
conn.send(command.encode('utf-8'))
print ("Commmand has been successfully. Waiting for confimation!")


data = conn.recv(16)

if data:
    print ("shutdown command has benn recieved and executed")
    print("")