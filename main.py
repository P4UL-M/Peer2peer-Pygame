from lib.pygame_menu import *
from var.globals import PATH
from client_main import server
from lib.tools import ConnRejected

game = Window("MySuperGame",Vector2(1000,800),PATH / "assets" / "bg.png")

principale = Menu("principale",childs=["Play"])

game.actual_menu = principale

#region main_menu
@principale.add_sprite
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

@principale.add_sprite
def play_button():
    _button = Button(
        name="Play",
        path=PATH / "assets" / "Empty_Node.png"
        )

    _button.set_position(Vector2(0.5,0.33))

    _button.set_text("Play",color="grey",padding=0.15)
    
    @_button.on_click
    def next_menu():
        game.actual_menu = principale.get_child("Play")

    return _button

@principale.add_sprite
def play_alert():
    _alert = AlertBox(
        name="Alert",
        path=PATH / "assets" / "Empty_Node.png",
        layer=1
        )

    _alert.padding = 0.1

    _alert.set_text(
        """Hello Word !
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam sollicitudin quam enim, at iaculis mauris congue nec. Curabitur sed massa id ante consectetur congue. Nam et est non sem pharetra varius quis vitae risus. Cras lectus enim, sodales ac neque a, pulvinar elementum ante. Nam pellentesque tincidunt ligula, a sagittis felis semper sit amet. Sed sagittis euismod tempor. Nulla facilisi.
        """,
        wrap_lenght=50,
        align_center=True)

    _alert.set_position(Vector2(0.5,0.33))
    _alert.set_scale(Vector2(1.5,2.0))

    @_alert.add_button
    def validate_button():
        _button = Button(
            name=f"validate_alert_{_alert.name}",
            path=PATH / "assets" / "Continue.png",
            layer=_alert.layer
        )
        
        _button.set_position(Vector2(0.5,1.0),parent=_alert)
        _button.set_scale(Vector2(0.5,0.5))

        @_button.on_click
        def close():
            _alert.isactive = False
            for _button in _alert.childs:
                _button.isactive = False
        
        return _button

    @_alert.on_enter
    def close():
        _alert.isactive = False
        for _button in _alert.childs:
            _button.isactive = False

    return _alert
#endregion

#region connection portal
secondaire = Menu("Play",parent="principale",childs="Connecting",background= PATH / "assets" / "bg_control.png")

@secondaire.add_sprite
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
        connecting.get_button("bad_conn").isactive = True

@secondaire.add_sprite
def validate_button():
    _button = Button(
        name="validate",
        path=PATH / "assets" / "Load.png"
    )
        
    _button.set_scale(Vector2(0.46,0.5))
    _button.set_position(Vector2(0.65,0.5))

    @_button.on_click
    def get_pseudo():
        game.actual_menu = secondaire.get_child("Connecting")
        connection_server(secondaire.get_button("pseudoBox").text)

    return _button

@secondaire.add_sprite
def pseudo_input():
    _inputbox = InputBox(
        name="pseudoBox",
        path = PATH / "assets" / "Empty_Node.png",
        paceHolder="Enter a pseudo...",
    )

    _inputbox.set_position(Vector2(0.5,0.3))

    @_inputbox.on_enter
    def start_menu():
        game.actual_menu = secondaire.get_child("Connecting")
        connection_server(_inputbox.text)

    return _inputbox
#endregion

#region connection wait screen
connecting = Menu("Connecting",parent="Play",childs="Online_Menu",background= PATH / "assets" / "bg_control.png")

@connecting.set_setup
def setup():
    connecting.get_button("bad_pseudo").isactive = False
    connecting.get_button("bad_conn").isactive = False

@connecting.add_sprite
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

@connecting.add_sprite
def bad_pseudo():
    _alert = AlertBox(
        name="bad_pseudo",
        path=PATH / "assets" / "Empty_Node.png",
        text_color="white",
        isactive=False
    )

    _alert.padding = 0.1

    _alert.set_position(Vector2(0.5,0.4))

    _alert.set_text("""BAD PSEUDO
    Le pseudo que vous avez choisi ne convient pas, veuillez en essayer un autre
    """,wrap_lenght=30,align_center=True)

    return _alert

@connecting.add_sprite
def bad_conn():
    _alert = AlertBox(
        name="bad_conn",
        path=PATH / "assets" / "Empty_Node.png",
        text_color="white",
        isactive=False
    )

    _alert.padding = 0.1

    _alert.set_position(Vector2(0.5,0.4))

    _alert.set_text("""CONNECTION FAILED
    La connexion au serveur a raté, veuillez vérifier votre accès à internet.
    """,wrap_lenght=30,align_center=True)

    return _alert

@server.Event
def bad_name(ctx):
    for button in connecting.buttons:
        if button.name == "bad_pseudo":
            button.isactive = True
    raise ConnRejected("The name you enter is incorrect")

@connecting.add_sprite
def back_button():
    _button = Button(
        name="back",
        path=PATH / "assets" / "Back_Button.png"
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

@online_menu.add_sprite
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

    @_button.Event(None)
    def disconnected():
        if not server.ready:
            game.actual_menu = online_menu.get_parent()

    return _button
#endregion

if __name__ == '__main__':
    try:
        game.run()
    except KeyboardInterrupt:  # interruption clavier CTRL-C: appel à la méthode destroy() de game.
        game.destroy()