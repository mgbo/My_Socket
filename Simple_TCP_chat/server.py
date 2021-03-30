
import threading
import socket

host = socket.gethostbyname(socket.gethostname())
#print (host)
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message): # client ရဲ့ nickname ကို client အားလုံးကို ပို့ရန်အတွက်
    for client in clients:
        client.send(message)

def handle(client): # 
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode('utf-8'))
            print (type(nickname), nickname)
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)
        print (f"nickname of clients is {nickname}!")

        broadcast(f"{nickname} joined the chat!".encode("utf-8")) # send message to all client
        client.send("Connected to the server!".encode('utf-8'))# send messaage to just conntected client

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print ("Server is listening....")
receive()













