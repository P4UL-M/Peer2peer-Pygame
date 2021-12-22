from lib.Class import *

server = Server()

@Client.Event
def set_name(self:Client,ctx):
    if ctx.name in server.Clients_list.keys():
        self.send_message("bad_name")
    else:
        self.client_name = ctx.name
        server.Clients_list[ctx.name] = self
        self.send_message("ready")

server.run()