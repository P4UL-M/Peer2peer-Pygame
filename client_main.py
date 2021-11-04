from bibliotheque.pygame_server_client import client

@client.Event
def bad_name(ctx):
    raise Exception("The name you enter is incorrect")

Main_Server = client