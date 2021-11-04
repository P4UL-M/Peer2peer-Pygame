from server_bibliotheque import *


@Client.Event("set_name")
def set_name(self,ctx):
    self.client_name = ctx.name

server = Server()
server.run()