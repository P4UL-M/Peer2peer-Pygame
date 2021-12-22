from sys import path
from lib.pygame_menu import *
from lib.tools import ConnRejected
from var.globals import GAME_INFO
import pygame
from os import path

directory = path.dirname(path.realpath(__file__))

GAME_INFO.GAME = game = Window("MySuperGame",Vector2(1000,800),f"{directory}/assets/bg.png")

principale = Menu("principale",childs=["Play"])

@principale.add_button
def exit_button():
    _button = Button(
        name="exit",
        path=f"{directory}/assets/Exit_Button.png"
        )

    _button.set_position(Vector2(0.5,0.66))
    #_button.set_scale(Vector2(10,2.0))

    @_button.Event(pygame.TEXTINPUT)
    def debug_some_shit(event):
        print(f"Vous avez pressé la touche : {event.text}, ce message vous a été envoyé depuis {_button.name} du menu {principale.name}")
    
    @_button.on_click
    def next_menu():
        game.destroy()

    return _button

@principale.add_button
def play_button():
    _button = Button(
        name="Play",
        path=f"{directory}/assets/Play.png"
        )

    _button.set_position(Vector2(0.5,0.33))
    #_button.set_scale(Vector2(10,2.0))
    
    @_button.on_click
    def next_menu():
        game.actual_menu = principale.get_child("Play")

    return _button

secondaire = Menu("Play",parent="principale",childs="Connecting",background=f"{directory}/assets/bg_control.png")

@secondaire.add_button
def back_button():
    _button = Button(
        name="back",
        path=f"{directory}/assets/Back_Button.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.35,0.5))

    @_button.on_click
    def back():
        game.actual_menu = secondaire.get_parent()

    return _button

@secondaire.add_button
def validate_button():
    _button = Button(
        name="validate",
        path=f"{directory}/assets/Load.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.65,0.5))

    @_button.on_click
    def get_pseudo():
        GAME_INFO.Main_Server.client_name = secondaire.get_button("pseudoBox").text
        GAME_INFO.Main_Server.run()
        game.actual_menu = secondaire.get_child("Connecting")

    return _button

@secondaire.add_button
def pseudo_input():
    _inputbox = InputBox(
        name="pseudoBox",
        path = f"{directory}/assets/Empty_Node.png",
        paceHolder="Enter a pseudo...",
    )

    _inputbox.set_position(Vector2(0.5,0.3))

    @_inputbox.on_enter
    def start_menu():
        GAME_INFO.Main_Server.client_name = _inputbox.text
        try:
            GAME_INFO.Main_Server.run()
        except ConnectionRefusedError:
            print("Error connection refused")
        game.actual_menu = secondaire.get_child("Connecting")

    return _inputbox

connecting = Menu("Connecting",parent="Play",childs="Online_Menu",background=f"{directory}/assets/bg_control.png")

@connecting.add_button
def connection():
    _button = Button(
        name="connecting",
        path=f"{directory}/assets/connecting.png"
    )
        
    _button.set_position(Vector2(0.5,0.4))

    @_button.Event(None)
    def check_ready():
        if GAME_INFO.Main_Server.ready:
            game.actual_menu = connecting.get_child("Online_Menu")

    return _button

@connecting.add_button
def bad_pseudo():
    _button = Button(
        name="bad_pseudo",
        path=f"{directory}/assets/Bad_Pseudo.png",
        isactive=False
    )
        
    _button.set_position(Vector2(0.5,0.4))

    return _button

@GAME_INFO.Main_Server.Event
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
        GAME_INFO.Main_Server.close()
        game.actual_menu = connecting.get_parent()

    return _button

online_menu = Menu("Online_Menu",parent="Play",background=f"{directory}/assets/bg_control.png")

@online_menu.add_button
def back_button():
    _button = Button(
        name="back",
        path=f"{directory}/assets/Back_Button.png"
    )
        
    _button.set_position(Vector2(0.5,0.66))

    @_button.on_click
    def back():
        GAME_INFO.Main_Server.close()
        game.actual_menu = online_menu.get_parent()

    return _button

game.actual_menu = principale

if __name__ == '__main__':
    try:
        game.run()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de game.
        game.destroy()