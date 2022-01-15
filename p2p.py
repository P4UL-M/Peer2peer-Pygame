import socket
from threading import Thread
import atexit

import miniupnpc

class Host(socket.socket):
    def __init__(self,host="0.0.0.0",port=61465):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (host,port)
        self.upnp = miniupnpc.UPnP()
        self.upnp.discoverdelay = 10

    def setup_port(self,state=True):
        self.upnp.discover()
        self.upnp.selectigd()
        try:
            if state:
                res = self.upnp.addportmapping(self.address[1], 'TCP', self.upnp.lanaddr, self.address[1], 'testing', '')    
            else:
                res = self.upnp.deleteportmapping(self.address[1], 'TCP')
            print("Port modifier" if res else "Error on port setup")
        except Exception:
            print("Error on port setup")

    def start(self):
        self.thread = Thread(target=self.run,daemon=True)
        self.thread.start()

    def run(self):
        self.bind(self.address)
        self.listen()
        self.setup_port()
        atexit.register(self.cleaning) #if the application close we stop the port
        try:
            self.handle()
        except:
            self.cleaning()

    def handle(self):
        self.peer, self.addr = self.accept()
        with self.peer as conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # launch event from here

    def cleaning(self):
        if self.upnp.getspecificportmapping(self.address[1], "TCP") is None:
            pass
        else:
            self.setup_port(False)

class Peer(socket.socket):
    def __init__(self,socket):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)