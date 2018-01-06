import threading
import os

class Order(threading.Thread):
	def __init__(self, app, data):
		super(Order, self).__init__()
		self.data = data
		self.app = app

	def xCmd(self):
		if(self.data == "fin"):
			self.app.go = False
		else :
			print("Execution commande", self.data)
			output = os.popen(self.data).read()
			print("result :", output)
			return output

	def run(self):
		if(self.data == "fin"):
			self.app.go = False
		elif(self.data.startswith("cmd ")):
			output = os.popen(self.data).read()
			print("result :", output)
			return output
