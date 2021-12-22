from lib.pygame_menu import Window

class Game_Info:
    def __init__(self):
        self.isplaying = False
        self.GAME:Window = None
        self.Main_Server = None
        self.Client = None
        self.party_conn = None


GAME_INFO = Game_Info()