
from PyQt5 import QtCore, QtWidgets
import client_ui
import connect_ui

import sys
import socket
import random

# for all client receive messages from all clients
class ReceiveThread(QtCore.QThread):
	signal = QtCore.pyqtSignal(str)

	def __init__(self, client_socket):
		super(ReceiveThread, self).__init__()
		self.client_socket = client_socket

	def run(self):
		while True:
			self.receive_message()

	def receive_message(self): # receive from other clients
		message = self.client_socket.recv(1024)
		message = message.decode()
		print (message) 
		self.signal.emit(message)


class Client:
	def __init__(self):
		self.messages = []
		self.main_window = QtWidgets.QWidget()

		# add widgets to the application window
		self.connectwidget = QtWidgets.QWidget(self.main_window)
		self.chatwidget = QtWidgets.QWidget(self.main_window)

		self.chatwidget.setHidden(True) # chat window ကို ပထမဦးဆုံး ဖျောက်ထား

		# --------------- connect widget for connection to server ------------
		self.connect_ui = connect_ui.Ui_Form()
		self.connect_ui.setupUi(self.connectwidget)
		self.connect_ui.pushButton.clicked.connect(self.btn_connect_clicked)

		# ------------------------- chat widget ---------------------
		self.chat_ui = client_ui.Ui_Form()
		self.chat_ui.setupUi(self.chatwidget)
		self.chat_ui.pushButton.clicked.connect(self.btn_send_clicked)

		# --------------- show main window ----------
		self.main_window.setGeometry(QtCore.QRect(1080, 20, 350, 500))
		self.main_window.show()

		# -------------- for socket ---------------
		self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# ------- to connect server -----------
	def btn_connect_clicked(self):
		host = self.connect_ui.hostTextEdit.toPlainText() # to get written letter in textedit field
		port = self.connect_ui.portTextEdit.toPlainText()
		nickname = self.connect_ui.nameTextEdit.toPlainText()
	
		if len(host) == 0:
			host = "localhost"

		if len(port) == 0:
			port = 5555
		else:
			try:
				port = int(port)

			except Exception as e:
				error = "Invalied port number\n {}".format(str(e))
				print ("[INFO]", error)
				self.show_error("Port Number Error", error)

		if len(nickname) < 1: # အကယ်၍ nickname ကို မရေးရင် computer name ကိုရယူရန်
			nickname = socket.gethostname()

		# nickname = nickname + "-" + str(random.randint(1,port))

		# after getting all the information, we will connect to the server
		if self.connect(host, port, nickname):
			self.connectwidget.setHidden(True)
			self.chatwidget.setVisible(True)

			self.recv_thread = ReceiveThread(self.tcp_client)
			self.recv_thread.signal.connect(self.show_message)
			self.recv_thread.start()
			print ("[INFO] recv thread started....")
		
	def show_message(self, message):
		self.chat_ui.textBrowser.append(message)

	def connect(self, host, port, nickname):
		try:
			self.tcp_client.connect((host, port))
			self.tcp_client.send(nickname.encode()) # Send nickname to server
			print ("[INFO] connected to server")
			return True
		except Exception as e:
			error = "Unable to connect to server \n'{}'".format(str(e))
			print("[INFO]", error)
			self.show_error("Connection Error", error)
			self.connect_ui.hostTextEdit.clear()
			self.connect_ui.portTextEdit.clear()			
			return False
	
	def btn_send_clicked(self):
		txt = self.chat_ui.textEdit.toPlainText()
		me_msg = "me : " + txt
		self.chat_ui.textBrowser.append(me_msg)
		self.chat_ui.textEdit.clear()
		print (me_msg)
		try:
			self.tcp_client.send(txt.encode())
		except Exception as e:
			error = "unable to send message '{}'".format(str(e))
			print ("[INFO]", error)
			self.show_error("Server Error", error)

	def show_error(self, error_type, message):
		errorDialog = QtWidgets.QMessageBox()
		errorDialog.setText(message)
		errorDialog.setWindowTitle(error_type)
		errorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
		errorDialog.exec_()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	c = Client()
	sys.exit(app.exec_())
