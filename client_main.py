from lib.Player_Sockets import Client
from var.globals import GAME_INFO

GAME_INFO.Main_Server = Main_Server = Client()

@Main_Server.Event
def fallback_response(ctx):
    pass
