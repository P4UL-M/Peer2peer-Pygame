import json
import socket
from time import time
from types import coroutine # seriously a comment for that ?
import json # well no need to explain
from threading import Thread # because we need multi-threading everywhere
import asyncio # why do we alway need coroutine, that's a good question

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
SERVER = None

class context:
    """
    class pour passer les infos du message rapidement
    """
    def __init__(self,peer,message):
        self.peer = peer
        for name,elt in message.items():
            setattr(self,name,elt)

class Client(socket.socket):
    """
    class discussion avec le server
    """
    handles:dict = {}

    def __init__(self,sock):
        # transfer the socket to the inherance
        super().__init__(fileno=sock.detach())
        self.client_name = ""
        # assignement of default variable
        self.ready = False
        # dict of all method for all possible event
        self.thread = Thread(target=self.run,daemon=True)
    
    def run(self):
        """
        Lance le server
        """
        self.send_message(event="get_name")
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
                    raise Exception("Connection has stopped")
                data = data.decode('utf-8')  
                print(f"<- {self.client_name} -",data)
                ctx = context(self,json.loads(data))
                if ctx.event in self.handles.keys():
                    self.handles[ctx.event](self,ctx)
        except Exception as e:
            print(f"diconnected from {self.client_name} : {e}")
            if self.client_name != "":
                del SERVER.Clients_list[self.client_name]

    def Event(func):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
        if func.__name__ not in Client.handles.keys():
            Client.handles[func.__name__] = func
        else:
            raise RuntimeError("the function you want to pass already exist")

class Server(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.Clients_list:dict[Client] = {}
        global SERVER
        SERVER = self

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
