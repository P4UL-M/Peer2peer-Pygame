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

class Client():
    """
    class discussion avec le server
    """
    handles:list = []
    _marker=object()

    def __init__(self,parent):
        # parent is the socket connection
        self._parent = parent
        self.client_name = ""
        # assignement of default variable
        self.ready = False
        # dict of all method for all possible event
        self.thread = Thread(target=self.handle,daemon=True)
       
    def __getattr__(self, name, default=_marker):
        if name in dir(self._parent):
            # Get it from papa:
            try:
                return getattr(self._parent, name)
            except AttributeError:
                if default is self._marker:
                    raise
                return default

        if name not in self.__dict__:
            raise AttributeError(name)
        return self.__dict__[name]  
    
    async def init(self):
        """
        Lance le server
        """
        self.send_message(event="get_name")
        self.thread.start()
        while self.client_name == "":
            pass
        return self.client_name

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
                for func in self.handles:
                    func(ctx.event,self,ctx)
        except Exception as e:
            print(f"diconnected from {self.client_name} : {e}")
            del SERVER.Clients_list[self.client_name]

    def Event(event):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
        self = Client
        def decorator(func):
            if event !=None or len([_func for _func in self.handles if _func.__name__==func.__name__])!=0:
                def wrap(_event,*args, **kwargs):
                    if _event == event:
                        func(*args, **kwargs)
                self.handles.append(wrap)
            else:
                print("you didn't specify the event or the function you want to pass already exist")
                raise RuntimeError
            return True
        return decorator

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
                myclient = Client(conn)
                Thread(target=self.init_client,args=(myclient,),daemon=True).start()
        except KeyboardInterrupt:
            for _client in self.Clients_list.values():
                _client.close()
            print("Bye !")
        
    def init_client(self,player:Client):
        print("New client initialization...")
        async def coroute():
            name = await player.init()
            if name in self.Clients_list.keys():
                player.send_message(event="Bad_Name")
                return
            self.Clients_list[name] = player
            player.send_message(event='ready')
        asyncio.run(coroute())
