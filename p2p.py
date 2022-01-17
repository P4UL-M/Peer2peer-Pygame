import socket,atexit,logging,json,miniupnpc
from threading import Thread

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

class context:
    """
    class pour passer les infos du message rapidement
    """
    def __init__(self,peer,message):
        self.peer = peer
        for name,elt in message.items():
            setattr(self,name,elt)

class ConnIterupted(Exception):
    """
    Execption when server reject connection
    """
    def __init__(self, *args: object,**kargs):
        super().__init__(*args,**kargs)

class Host(socket.socket):
    
    handles:dict = {}
    
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
        except Exception as e:
            logging.info(f"Disconnected from peer {self.peer}, thread will stop.\n\ Error : {e}")
            
    def handle(self):
        self.peer, self.addr = self.accept()
        print("connection")
        with self.peer as conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    raise ConnIterupted("Connection has stopped")
                data = data.decode('utf-8')
                ctx = context(self,json.loads(data))
                if ctx.event in self.handles.keys():
                    self.handles[ctx.event](self,ctx)

    def cleaning(self):
        if self.upnp.getspecificportmapping(self.address[1], "TCP") is None:
            return None
        else:
            return self.setup_port(False)

    def Event(self,func):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
        if func.__name__ not in self.handles.keys():
            self.handles[func.__name__] = func
        else:
            raise RuntimeError("the function you want to pass already exist")

    def send_message(self,event,args=dict()):
        """
        Fonction d'envoie de message
        """
        if event=='':
            return
        message = {
            'event':event
        }
        message.update(args)
        message = json.dumps(message)
        print(f"- {self.client_name} ->",message)
        data = str.encode(message)
        self.sendall(data)

class Peer(socket.socket):
    
    handles:dict = {}
 
    def __init__(self,host,port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (host,port)

    def start(self):
        self.thread = Thread(target=self.run,daemon=True)
        self.thread.start()

    def run(self):
        self.connect(self.address)
        try:
            self.handle()
        except Exception as e:
            logging.info(f"Disconnected from peer {self.peer}, thread will stop.\n\ Error : {e}")
                 
    def handle(self):
        while True:
            data = self.recv(1024)
            if not data:
                raise ConnIterupted("Connection has stopped")
            data = data.decode('utf-8')
            ctx = context(self,json.loads(data))
            if ctx.event in self.handles.keys():
                self.handles[ctx.event](self,ctx)

    def Event(self,func):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
        if func.__name__ not in self.handles.keys():
            self.handles[func.__name__] = func
        else:
            raise RuntimeError("the function you want to pass already exist")

    def send_message(self,event,args=dict()):
        """
        Fonction d'envoie de message
        """
        if event=='':
            return
        message = {
            'event':event
        }
        message.update(args)
        message = json.dumps(message)
        print(f"- {self.client_name} ->",message)
        data = str.encode(message)
        self.sendall(data)
