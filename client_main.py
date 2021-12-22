from os import name
from lib.Player_Sockets import Client
from var.globals import GAME_INFO

GAME_INFO.Main_Server = Main_Server = Client(pseudo="Poool")

@Main_Server.Event
def conn_accepted(ctx):
    Main_Server.ready = True
    print("connected and ready !")


@Main_Server.Event
def fallback_response(ctx):
    pass

GAME_INFO.Main_Server.run()

while True:
    pass