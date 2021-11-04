from sys import path
from bibliotheque.pygame_menu import *
from client_main import Main_Server
import pygame
from os import path

directory = path.dirname(path.realpath(__file__))

game = Window("MySuperGame",Vector2(1000,800),f"{directory}/assets/bg.png")

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
        Main_Server.client_name = secondaire.get_button("pseudoBox").text
        Main_Server.run()
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
        Main_Server.client_name = _inputbox.text
        Main_Server.run()
        game.actual_menu = secondaire.get_child("Connecting")

    return _inputbox

connecting = Menu("Connecting",parent="Play",childs="Online_Menu")

@connecting.add_button
def connection():
    _button = Button(
        name="connecting",
        path=f"{directory}/assets/connecting.png"
    )
        
    #_button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.5,0.5))

    @_button.Event(None)
    def check_ready():
        if Main_Server.ready:
            game.actual_menu = connecting.get_child("Online_Menu")

    return _button

online_menu = Menu("Online_Menu",parent="Play")

@online_menu.add_button
def back_button():
    _button = Button(
        name="back",
        path=f"{directory}/assets/Back_Button.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.35,0.5))

    @_button.on_click
    def back():
        Main_Server.close()
        game.actual_menu = online_menu.get_parent()

    return _button

game.actual_menu = principale

if __name__ == '__main__':
    try:
        game.run()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de game.
        game.destroy()