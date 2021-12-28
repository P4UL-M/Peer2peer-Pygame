from sys import path
from lib.pygame_menu import *
from var.globals import PATH
from client_main import server
from lib.tools import ConnRejected
import pygame
from os import path

directory = path.dirname(path.realpath(__file__))

game = Window("MySuperGame",Vector2(1000,800),PATH / "assets" / "bg.png")

principale = Menu("principale",childs=["Play"])

pygame.font.init()
font = pygame.font.SysFont("Sans", 22)

@principale.add_button
def exit_button():
    _button = Button(
        name="exit",
        path= PATH / "assets" / "Exit_Button.png"
        )

    _button.set_position(Vector2(0.5,0.66))

    @_button.on_click
    def next_menu():
        game.destroy()

    return _button

@principale.add_button
def play_button():
    _button = Button(
        name="Play",
        path=PATH / "assets" / "Play.png"
        )

    _button.set_position(Vector2(0.5,0.33))
    
    @_button.on_click
    def next_menu():
        game.actual_menu = principale.get_child("Play")

    return _button

@principale.add_button
def play_alert():
    _alert = AlertBox(
        name="Alert",
        path=PATH / "assets" / "Empty_Node.png"
        )

    _alert.set_text("Joueur et Joueuse :\nJ'ai l'honneur de vous annoncer l'arrivé de ce nouveaux jeu incroyable merci pour votre soutien.",wrap_lenght=50,align_center=True)

    _alert.set_scale(Vector2(1.5,2.0))
    _alert.set_position(Vector2(0.5,0.33))

    
    @_alert.on_enter
    def close():
        _alert.isactive = False

    return _alert

#region connection portal
secondaire = Menu("Play",parent="principale",childs="Connecting",background= PATH / "assets" / "bg_control.png")

@secondaire.add_button
def back_button():
    _button = Button(
        name="back",
        path=PATH / "assets" / "Back_Button.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.35,0.5))

    @_button.on_click
    def back():
        game.actual_menu = secondaire.get_parent()

    return _button

def connection_server(name):
    server.client_name = name
    try:
        server.run()
    except ConnectionRefusedError:
        connecting.get_button("bad_pseudo").isactive = True

@secondaire.add_button
def validate_button():
    _button = Button(
        name="validate",
        path=PATH / "assets" / "Load.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.65,0.5))

    @_button.on_click
    def get_pseudo():
        connection_server(secondaire.get_button("pseudoBox").text)
        game.actual_menu = secondaire.get_child("Connecting")

    return _button

@secondaire.add_button
def pseudo_input():
    _inputbox = InputBox(
        name="pseudoBox",
        path = PATH / "assets" / "Empty_Node.png",
        paceHolder="Enter a pseudo...",
    )

    _inputbox.set_position(Vector2(0.5,0.3))

    @_inputbox.on_enter
    def start_menu():
        connection_server(_inputbox.text)
        game.actual_menu = secondaire.get_child("Connecting")

    return _inputbox
#endregion

#region connection wait screen
connecting = Menu("Connecting",parent="Play",childs="Online_Menu",background= PATH / "assets" / "bg_control.png")

@connecting.add_button
def connection():
    _button = Button(
        name="connecting",
        path=PATH / "assets" / "connecting.png"
    )
        
    _button.set_position(Vector2(0.5,0.4))

    @_button.Event(None)
    def check_ready():
        if server.ready:
            game.actual_menu = connecting.get_child("Online_Menu")

    return _button

@connecting.add_button
def bad_pseudo():
    _button = Button(
        name="bad_pseudo",
        path=PATH / "assets" / "Bad_Pseudo.png",
        isactive=False
    )
        
    _button.set_position(Vector2(0.5,0.4))

    return _button

@server.Event
def bad_name(ctx):
    for button in connecting.buttons:
        if button.name == "bad_pseudo":
            button.isactive = True
    raise ConnRejected("The name you enter is incorrect")

@connecting.add_button
def back_button():
    _button = Button(
        name="back",
        path=f"{directory}/assets/Back_Button.png"
    )
        
    _button.set_scale(Vector2(0.5,0.5))
    _button.set_position(Vector2(0.5,0.65))

    @_button.on_click
    def back():
        server.close()
        game.actual_menu = connecting.get_parent()

    return _button
#endregion

#region online menu
online_menu = Menu("Online_Menu",parent="Play",background= PATH / "assets" / "bg_control.png")

@online_menu.add_button
def back_button():
    _button = Button(
        name="back",
        path=PATH / "assets" / "Back_Button.png"
    )
        
    _button.set_position(Vector2(0.5,0.66))

    @_button.on_click
    def back():
        server.close()
        game.actual_menu = online_menu.get_parent()

    return _button
#endregion

game.actual_menu = principale

if __name__ == '__main__':
    try:
        game.run()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de game.
        game.destroy()