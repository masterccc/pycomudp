#!/usr/bin/env python3

from app import *
from order import *
from gui import *

import threading

class Cmd(threading.Thread):
	def __init__(self, srv):
		threading.Thread.__init__(self)
		self.server = srv
		self.go = True
	def run(self):
		while(self.go):
			cmd = input(">")
			self.server.sendAll(cmd)
		print("End of cmd thread")
	def finish(self):
		self.go = False

def main():

	me = AppThread()
	if(me.apptype == AppType.SRV):
		windou = Fenetre(me)
		me.setGUI(windou)
		me.start()
		windou.mainloop()

	else:
		print("Waiting master orders")
		me.start()

if __name__ == "main":
	main()

main()
