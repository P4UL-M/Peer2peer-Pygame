import json
from socket import socket,AF_INET,SOCK_STREAM
from threading import Thread # because we need multi-threading everywhere
from var.globals import HOST,PORT

_server = None

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

class Client(socket):
    """
    class discussion avec le server
    """
    handles:dict = {}

    def __init__(self,sock):
        # transfer the socket to the inherance
        super().__init__(fileno=sock.detach())
        self.client_name = ""
        self.address = None
        # assignement of default variable
        self.ready_play = False
        # dict of all method for all possible event
        self.thread = Thread(target=self.run,daemon=True)
    
    def run(self):
        """
        Lance le server
        """
        self.handle()

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
    
    def handle(self):
        """
        récupère et traite les évènement
        """
        try:
            while True:
                data = self.recv(1024)
                if not data:
                    raise ConnIterupted("Connection has stopped")
                data = data.decode('utf-8')
                ctx = context(self,json.loads(data))
                if ctx.event in self.handles.keys():
                    self.handles[ctx.event](self,ctx)
        except Exception as e:
            print(f"diconnected from {self.client_name} : {e}")
            if self.client_name in _server.Clients_list.keys():
                del _server.Clients_list[self.client_name]

    def Event(func):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
        if func.__name__ not in Client.handles.keys():
            Client.handles[func.__name__] = func
        else:
            raise RuntimeError("the function you want to pass already exist")

class Server(socket):
    def __init__(self):
        super().__init__(AF_INET, SOCK_STREAM)
        self.Clients_list:dict[Client] = {}
        global _server
        _server = self

    def run(self):
        try:
            self.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
        print('Socket is listening..')
        self.Handle()

    def Handle(self):
        try:
            while True:
                # écoute de nouvelles connections 
                self.listen()
                # acceptation de la demande de connection entrante
                conn, address = self.accept()
                # nouveau objet client (and not Client, we take the update class with the handle method)
                print("New client initialization...")
                myclient = Client(conn)
                myclient.thread.start()
        except KeyboardInterrupt:
            for _client in self.Clients_list.values():
                _client.close()
            print("Bye !")
