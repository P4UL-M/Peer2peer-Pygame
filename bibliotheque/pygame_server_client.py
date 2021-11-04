import socket # seriously a comment for that ?
#from requests import get # to get global ip, maybe not necessary after
import json # well no need to explain
from threading import Thread # because we need multi-threading everywhere
from _thread import interrupt_main #to stop just this programme from a thread

class context:
    """
    class pour passer les infos du message rapidement
    """
    def __init__(self,peer,message):
        self.peer = peer
        for name,elt in message.items():
            setattr(self,name,elt)

# class inherit from socket so all that a socket can do, this class can also do
class Client(socket.socket):
    """
    class discussion avec le server
    """
    def __init__(self):
        # init of the socket class inherit
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        #constants
        self.client_name = ""
        #self.EXTERNAL_IP = get("https://api.ipify.org").text
        self.HOST = 'localhost'  # The server's hostname or IP address
        self.PORT = 65432        # The port used by the server
        # assignement of default variable
        self.ready = False
        # dict of all method for all possible event
        self.handles:list[function] = []
        self.thread = Thread(target=self.handle,daemon=True)
           
    def run(self):
        """
        Lance le server
        """
        print("connecting at",self.HOST,"on port",self.PORT,"...")
        self.connect((self.HOST, self.PORT))
        self.thread.start()

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
        print("->",message)
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
                    if self.fileno()==-1:
                        raise ConnectionResetError
                    else:
                        continue
                data = data.decode('utf-8')  
                print("<- ",data)
                ctx = context(self,json.loads(data))
                if not self.ready:
                    try:
                        for func in self.handles:
                            func(ctx.event,ctx)
                    except RuntimeWarning as e: 
                        print(f"ERROR WITH THE INITIALISATION WITH SERVER : {e}")
                    except e:
                        print(e)
                else:
                    for func in self.handles:
                        func(ctx.event,ctx)
        except:
            print(f"diconnected from {self.HOST}")
            self.destroy()

    def Event(self,event):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        """
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

    def destroy(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = Thread(target=self.handle,daemon=True)
        self.ready = False
        self.client_name = ""

client = Client()

@client.Event("get_name")
def get_name(ctx):
    if client.client_name == "":
        raise RuntimeWarning("You must specify a pseudo before running the client")
    else:
        print(client.client_name)
    client.send_message('set_name',{'name':client.client_name})
    
@client.Event("ready")
def ready(ctx):
    client.ready = True
