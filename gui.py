#!/usr/bin/env python3


from tkinter import *
import threading

class PeerLine(PanedWindow):
	def __init__(self, mother, win, pid, ip, port):
		super(PeerLine, self).__init__(win, orient=HORIZONTAL)
		self.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

		self.mother = mother 
		self.pid= pid
		self.ip = ip
		self.port = str(port)

		self.btnDel = Button(win, text="delete", width=2, command=lambda: self.mother.requestRemove(self.pid) )
		
		self.lbl_id = Label(win, text=pid )
		self.lbl_ip = Label(win, text=ip )
		self.lbl_port = Label(win, text=port )
		
		self.result = Entry(self, textvariable="Cmd result", width=50)
		self.result.pack()

		self.lbl_id.pack()
		self.lbl_ip.pack()
		self.lbl_port.pack()
		
		self.add( self.lbl_id)
		self.add( self.lbl_ip)
		self.add( self.lbl_port)
		self.add( self.result)

		self.add( self.btnDel)


class Fenetre(Tk, threading.Thread):
	def __init__(self, netthread):
		
		Tk.__init__(self)
		threading.Thread.__init__(self)

		self.peerlist = list()

		lbl_titlepeers = Label(self, text="Connected peers")
		lbl_titlepeers.pack()

		self.cmdinput = Entry(self, textvariable="Command", width=50)
		self.cmdinput.pack()

		self.btnSend = Button(self, text="Send" ,command=self.requestSend)
		self.btnSend.pack()

		self.peersLabel = LabelFrame(self, text="Connected peers", padx=20, pady=20)
		self.peersLabel.pack(fill="both", expand="yes")
		
		self.server = netthread

		btnQuit = Button(self, text="Exit", command=self.quitter)
		btnQuit.pack()

	def quitter(self):
		self.server.closeServer()
		self.destroy()
		self.quit()

	def run(self):
			self.mainloop()

	def addPeer(self,ppid, ip, port):
		newp = PeerLine(self, self.peersLabel, str(ppid), str(ip), str(port))
		newp.pack()
		self.peerlist.append(newp)


	def requestSend(self):
		self.server.sendAll(self.cmdinput.get())

	def requestRemove(self, ppid):
		for peer in self.peerlist:
			if(peer.pid == ppid):
				peer.lbl_port['text'] = 'KICKED'
				peer.lbl_port.configure(foreground="red")
				peer.pack()
				cleaned_list = [ x for x in self.peerlist if x.pid is not ppid ]
				self.peerlist = cleaned_list
		self.server.kick(ppid)
	
	def setResponse(self, ppid, response):
		for peer in self.peerlist:
			if(str(peer.pid) == str(ppid)):
				peer.result.delete(0,END)
				peer.result.insert(0,response)
