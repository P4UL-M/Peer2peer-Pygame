import socket
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
        if state:
            res = self.upnp.addportmapping(self.address[1], 'TCP', self.upnp.lanaddr, self.address[1], 'testing', '')    
        else:
            res = self.upnp.deleteportmapping(self.address[1], 'TCP')
        
        print("Port modifier" if res else "Error on port setup")

    def run(self):
        self.bind(self.address)
        self.listen()
        self.setup_port()
        try:
            self.handle()
        except KeyboardInterrupt:
            self.setup_port(False)
            print("Bye")

    def handle(self):
        conn, addr = self.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

class Peer(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)