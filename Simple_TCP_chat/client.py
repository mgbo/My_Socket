
import socket
import threading

nickname = input("Choose a nickname: ")

host = socket.gethostbyname(socket.gethostname())
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def recive():
	while True:
		try:
			message = client.recv(1024).decode('utf-8')
			if message == 'NICK':
				client.send(nickname.encode('utf-8'))
			else:
				print ("Message : ", message)
		except:
			print ("An error occured")
			client.close()
			break

def write():
	while True:
		message = f"{nickname}: {input()}"
		client.send(message.encode('utf-8'))


write_thread = threading.Thread(target=write)
write_thread.start()

recive_thread = threading.Thread(target=recive)
recive_thread.start()







