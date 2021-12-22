import json
import socket
from threading import Thread
from var.globals import *

class Server(socket.socket):
    def __init__(self,Port,Client):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.PORT = Port
        self.Client_a = None
        self.Client_b = None

    def run(self):
        try:
            self.bind((HOST, self.PORT))
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
                #myclient = Client(conn)
                #myclient.thread.start()
        except KeyboardInterrupt:
            for _client in self.Clients_list.values():
                _client.close()
            print("Bye !")
