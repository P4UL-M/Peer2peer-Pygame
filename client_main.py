from bibliotheque.pygame_server_client import Client

Main_Server = Client()

@Main_Server.Event
def get_name(ctx):
    if Main_Server.client_name == "":
        Main_Server.handles["bad_name"](None)
        raise Exception("You must specify a pseudo before running the client")
    Main_Server.send_message('set_name',{'name':Main_Server.client_name})
    
@Main_Server.Event
def ready(ctx):
    Main_Server.ready = True
