import socket
import threading
import sys
from order import Order
from random import random
from enum import Enum

UDP_IP = "255.255.255.255"
UDP_PORT = 5005

peers = list()

def introduce(port):
  s = "listen " + str(port)
  return s.encode()


class AppType(Enum):
  SRV = 0
  CLI = 1

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
    
class AppThread(threading.Thread):
  def __init__(self):

    super(AppThread, self).__init__()
    self.sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock_out.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    self.go = True
    self.cpid = 0
    self.apptype = AppType.SRV
    self.grap = False

    try:
      self.sock_in = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
      self.sock_in.bind((UDP_IP, UDP_PORT))
    except OSError: 
      cport = int(random()*(65000-1024) + 1024)
      print("Client (listen on (", cport, ")")
      self.apptype = AppType.CLI
      bin = self.sock_in.bind((get_ip_address(), cport))
      self.sock_out.sendto(introduce(cport), (UDP_IP, UDP_PORT))


  def send(self, msg):
    self.sock_out.sendto(msg.encode(), ('255.255.255.255', 5005))      
 

  def sendToId(self, ppid, msg):
    for peer in peers :
      if( str(peer[0]) == str(ppid)):
        self.sock_out.sendto(msg.encode(), peer[1])
        break
        
  def kick(self, ppid):
    print("kick : ", ppid)
    self.sendToId(ppid, "fin")

  def sendAll(self, msg):
    for peer in peers :
      self.sock_out.sendto(msg.encode(), peer[1])

  def closeServer(self):
    print("Closing Server & socket")
    self.sendAll("fin")
    print("fin")
    self.go = False
    try:
      self.sock_in.shutdown(socket.SHUT_RDWR)
    except OSError:
      pass
    try:
      self.sock_out.shutdown(socket.SHUT_RDWR)
    except OSError:
      pass
    self.sock_in.close()
    self.sock_out.close()
    self.grap.quit()


  def run(self):

      while(self.go):
        try:
          print("Listening...")
          data, addr = self.sock_in.recvfrom(1024) # buffer size is 1024 bytes
          data = data.decode("utf-8")
          print("rcv :", data, "from" , addr)
        
        except OSError:
          closeServer()

        if(self.apptype == AppType.SRV):
          if(data.startswith("listen")):
            if addr[0] not in peers:
              dport = int(data.split(" ")[1])
              peers.append([self.cpid, (addr[0],dport)])
              self.grap.addPeer(self.cpid, str(addr[0]), dport)
              print((addr[0],dport), "Added to node list : ",self.cpid, str(addr[0]), dport)
              self.sock_out.sendto("ADDED".encode(), (addr[0], dport))
              self.cpid += 1

          elif(data.startswith("result")):
            for p in peers:
              print(p)

            ppid = [ x for x in peers if x[1][0] == addr[0] ][0][0]
            print("Result come from  " , addr, "pid : ", ppid)
            self.grap.setResponse(ppid,data)
          else:
            print("Unknown client")

            ## CLIENT
        elif(data.startswith("cmd ")):
          parse = " ".join(data.split(" ")[1:])
          ordre = Order(self, parse)
          seres = ordre.xCmd()
          response = "result " + str(seres)
          self.send(response)
          print("Result reçu : " , seres)

        elif(data.startswith("fin")):
          self.go = False
          print("Disconnect")

      print("End of AppThread")


  def setGUI(self, gui):
    print("Application du setgui")
    self.grap = gui
    

