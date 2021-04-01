
import socket
import threading

class Server:
	def __init__(self, host, port):
		self.clients = {}

		self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# to reuse the same host name and port number
		self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.tcp_server.bind((host, port))
		self.tcp_server.listen(5)

		print ("[INFO] Server running on {}:{}".format(host, port))

		while True:
			conn, addr = self.tcp_server.accept()

			nickname = conn.recv(1024) # to receive nickname of new client
			nickname = nickname.decode()
			self.clients[nickname] = conn
	
			# start a thread to get message from all client in the server
			receive_thread = threading.Thread(target=self.receive_message, args=(conn, nickname), daemon=True)
			receive_thread.start()

			print ("Connection from {}:{} with name {}".format(addr[0], addr[1], nickname))

	def receive_message(self, connection, nickname):
		print("[INFO] waiting for messages")
		while True:
			try:
				msg = connection.recv(1024) # server receive message from clients
				self.send_message(msg, nickname) # server send message to all clients
				print (nickname + ':' + msg.decode())
			except:
				connection.close()
				del(self.clients[nickname]) # remove user from users list
				break
		print(nickname, "is disconnected")
	
	def send_message(self, message, sender):
		if len(self.clients) > 0:
			for nickname in self.clients: # to get values(nickname) from clients dict
				if nickname != sender:
					msg = sender + ":" + message.decode()
					self.clients[nickname].send(msg.encode())
					


if __name__ == "__main__":
	Server('localhost', 5555)



