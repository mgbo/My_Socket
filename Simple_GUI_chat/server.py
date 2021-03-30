
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


clients = []
nicknames = []

# Broadcast
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print (f"{nicknames[clients.index(client)]}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print (f"Connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8') # .decode('utf-8')

        clients.append(client)
        nicknames.append(nickname)

        print(f"Nickname of the clients is {nickname}")
        
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8')) # client အားလုံးကိုပို့
        client.send("Conntected to the server!".encode('utf-8')) # အသစ် joint လာတဲ့ client ကိုဘဲပို့

        # handle(client)
        
        thread = threading.Thread(target=handle, args=(client,)) # receive message နှင့် send message အတွက်  
        thread.start()

        # print (clients)
        # print (nicknames)

print ("server is listening...")
receive()








