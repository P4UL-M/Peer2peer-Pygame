from lib.Player_Sockets import Client

server = Client()


@server.Event
def conn_accepted(ctx):
    server.ready = True
    print("connected and ready !")


@server.Event
def fallback_response(ctx):
    pass
