
import socket
import time

host, port = "127.0.0.1", 25001


listensocket = socket.socket()
listensocket.bind((host, port))
listensocket.listen()



startPos = [0, 0, 0] #Vector3   x = 0, y = 0, z = 0


print ("Python server is listenning to Unity client.....")
# clientsocket, address = listensocket.accept()
# print ("Unity client has been established....")


# clientsocket.sendall('25,0, 10'.encode('utf-8'))

while True:
    clientsocket, address = listensocket.accept()
    while True:
        time.sleep(0.5) #sleep 0.5 sec
        startPos[0] +=1 #increase x by one
        posString = ','.join(map(str, startPos)) #Converting Vector3 to a string, example "0,0,0"
        print(posString) # 1,0,0

        clientsocket.sendall(posString.encode("UTF-8")) #Converting string to Byte, and sending it to C#
        receivedData = clientsocket.recv(1024).decode("UTF-8") #receiveing data in Byte fron C#, and converting it to String
        print(receivedData) # hey i got your message python! do you see this message?