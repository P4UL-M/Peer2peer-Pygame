from bibliotheque.pygame_server_client import client

@client.Event("Bad_Name")
def bad_name(ctx):
    print("Connection refused")
    raise ConnectionResetError

Main_Server = client