from var.globals import PATH
from lib.Player_Sockets import *
import json

SETTINGS = json.load(open(PATH / "assets" / "Setting.json"))

Host = SETTINGS["global_server_url"]
Port = SETTINGS["global_server_port"]

server = Client(Host,Port)

@server.Event
def conn_accepted(ctx):
    server.ready = True
    print("connected and ready !")

@server.Event
def fallback_response(ctx):
    pass