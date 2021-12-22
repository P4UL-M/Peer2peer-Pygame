from lib.Class import *
from var.globals import VARIABLES

server = Server()

@Client.Event
def connection(self:Client,ctx):
    if ctx.name in server.Clients_list.keys():
        self.send_message("bad_name")
    else:
        self.client_name = ctx.name
        server.Clients_list[ctx.name] = self
        self.send_message("conn_accepted")

@Client.Event
def set_adr(self:Client,ctx):
    if ctx.fallback == False:
        self.address = ctx.address
        self.ready_play = True
    else:
        #fallback.run
        #self.address = fallback
        #self.ready_play
        #send_newaddress
        pass

server.run()