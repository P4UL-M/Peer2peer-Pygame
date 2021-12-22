import pygame as py
from bibliotheque.basics_class import Vector2,attr_exist
from pygame.locals import *     # PYGAME constant & functions
from sys import exit            # exit script 
from time import time


_window = None

class Window():
    """
    class principale de pygame qui gère la fenetre
    """
    def __init__(self,name,size:Vector2,background) -> None:
        """
        initialisation de pygame et de la fenêtre et des variables globales
        """
        py.init()   
        self.screen:py.Surface = py.display.set_mode((size.x, size.y),0,32)
        py.display.set_caption(name)

        self.actual_menu:Menu = None
        self.menus:list[Menu] = []
        # ******** le background devrait etre gérer indivituellement pour les menu en option pour overidecelui là
        try:
            self.background = py.image.load(background).convert() # tuile pour le background
            self.background = py.transform.scale(self.background, (size.x, size.y))
        except FileNotFoundError:
            print("Your principal background doesn't seems to exist")   
        
        global _window
        _window = self
    
    def run(self):
        """
        fonction principale du jeu qui gère la fenetre
        """
        while True:
            if self.actual_menu.background == None:
                self.screen.blit(self.background,(0,0))
            else:
                self.screen.blit(self.actual_menu.background,(0,0))
            self.actual_menu.Update()
            py.display.update()

    def destroy(self):
        """
        destructeur de la classe
        """
        print('Bye!')
        py.quit()   # ferme la fenêtre principale
        exit()      # termine tous les process en cours

class Button:
    """
    classe de bouton simple avec méthode rapide pour Event et On_Click
    """
    def __init__(self,name,path,isactive=True):
        self.name = name
        self.file = path
        self.position = Vector2(0,0)
        self.rect = None
        self.isactive = isactive
        
        self.handles = []
        try:
            self.surface:py.Surface = py.image.load(self.file).convert_alpha()
        except FileNotFoundError:
            print("Your type of button doesn't seems to exist")

    def Event(self,event):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si l'évènement est appellé.
        Si l'event passé est nulle alors la fonction est attribué à la fonction Update executé
        juste avant l'affichage
        """
        def decorator(func):
            if event !=None:
                def wrap(_event:py.event.Event,*args, **kwargs):
                    if _event.type == event:
                        return func(_event,*args, **kwargs)
                    else:
                        return self.empty
                self.handles.append(wrap)
            else:
                def wrap(*args, **kwargs):
                    if self.isactive:
                        return func(*args,**kwargs)
                setattr(self,"Update",wrap)
            return True
        return decorator

    def set_position(self,pos:Vector2,TopLeft=False):
        """
        attribue les valeur du vecteur à la position de l'image, si les valeur sont en float alors elle sont considérer comme un multiplicateur
        """
        x,y = None,None
        if TopLeft:
            if type(pos.x)==float:
                x = int(_window.screen.get_width()*pos.x)
            if type(pos.y)==float:
                y = int(_window.screen.get_height()*pos.y)
        else:
            x = pos.x - self.surface.get_width()/2
            y = pos.y - self.surface.get_height()/2
            if type(pos.x)==float:
                x = int(_window.screen.get_width()*pos.x - self.surface.get_width()/2)
            if type(pos.y)==float:
                y = int(_window.screen.get_height()*pos.y - self.surface.get_height()/2)
        self.position:Vector2 = Vector2(x or pos.x,y or pos.y)
        self.set_rect(Vector2(x or pos.x,y or pos.y))
    
    def set_scale(self,sca:Vector2):
        """
        attribue les valeur du vecteur à la taille de l'image, si les valeur sont en float alors elle sont considérer comme un multiplicateur
        """
        # bug de position lors du rescale prise en compte necessaire du monde de placement choisit c'est la merde xd
        x,y = None,None
        if type(sca.x)==float:
            x = int(self.surface.get_width()*sca.x)
        if type(sca.y)==float:
            y = int(self.surface.get_height()*sca.y)
        self.surface = py.transform.scale(self.surface,(x or sca.x,y or sca.y))
        #self.set_position(Vector2(self.position.x,self.position.y),TopLeft=True)

    def set_rect(self,coord:Vector2):
        self.rect = self.surface.get_rect(topleft=(coord.x,coord.y))

    def on_click(self,func):
        """
        nouvelle fonction qui n'executera que la fonction en cas de click du boutton
        la nouvelle fonction est ajouté dans la liste des function à executé et dans la classe
        cette partie peut etre enleve plus tard car inutile et permet de ne plus vérifier l'existance
        """
        def wrap(_event:py.event.Event,*args,**kargs):         
            if _event.type == py.MOUSEBUTTONUP:
                if self.rect.collidepoint(py.mouse.get_pos()):
                    return func(*args,**kargs)
        self.handles.append(wrap)
        return True

    def Handle(self,*arg,**kargs):
        if self.isactive:
            for func in self.handles:
                func(*arg,**kargs)
 
    def draw(self,ecran):
        if self.isactive:
            ecran.blit(self.surface,(self.position.x,self.position.y))

    def Update(*args,**kargs): ...

    def empty(*args,**kargs): ...

class InputBox:
    """
    class de InputBox autonome, permet de rentrer du texte facilement
    """
    def __init__(self,name,path,paceHolder='Enter text...',color='black',text_color='grey',alter_text_color="white",max_char=16,isactive=True):
        self.name = name
        self.file = path
        self.position:Vector2 = Vector2(0,0)
        self.rect = None
        self.isactive = isactive
        
        try:
            self.surface:py.Surface = py.image.load(self.file).convert_alpha()
        except FileNotFoundError:
            print("Your file for InputBox doesn't seems to exist")

        self.color = Color(color)
        self.text = ''
        self.paceHolder = paceHolder
        self.max_char = max_char
        self.text_color = Color(text_color)
        self.text_color_inactive = Color(text_color)
        self.text_color_active = Color(alter_text_color)

        self.text_size = self.get_text_size()

        self.FONT = py.font.Font(None,self.text_size)
        self.txt_surface = self.FONT.render(self.paceHolder, True, self.text_color)
        self.active = False

    def get_text_size(self):
        i = self.surface.get_height()
        temp = py.font.Font(None,i)
        size_temp = temp.size("A"*self.max_char)
        while int(self.surface.get_height()*0.80)<size_temp[1] or int(self.surface.get_width()*0.9)<size_temp[0]:
            i -=1
            temp = py.font.Font(None,i)
            size_temp = temp.size("A"*self.max_char)
        return(i)

    def set_position(self,pos:Vector2,TopLeft=False):
        """
        attribue les valeur du vecteur à la position de l'image, si les valeur sont en float alors elle sont considérer comme un multiplicateur
        """
        x,y = None,None
        if TopLeft:
            if type(pos.x)==float:
                x = int(_window.screen.get_width()*pos.x)
            if type(pos.y)==float:
                y = int(_window.screen.get_height()*pos.y)
        else:
            x = pos.x - self.surface.get_width()/2
            y = pos.y - self.surface.get_height()/2
            if type(pos.x)==float:
                x = int(_window.screen.get_width()*pos.x - self.surface.get_width()/2)
            if type(pos.y)==float:
                y = int(_window.screen.get_height()*pos.y - self.surface.get_height()/2)
        self.position:Vector2 = Vector2(x or pos.x,y or pos.y)
        self.set_rect(Vector2(x or pos.x,y or pos.y))

    def set_scale(self,sca:Vector2):
        """
        attribue les valeur du vecteur à la taille de l'image, si les valeur sont en float alors elle sont considérer comme un multiplicateur
        """
        # bug de position lors du rescale prise en compte necessaire du monde de placement choisit c'est la merde xd
        x,y = None,None
        if type(sca.x)==float:
            x = int(self.surface.get_width()*sca.x)
        if type(sca.y)==float:
            y = int(self.surface.get_height()*sca.y)
        self.surface = py.transform.scale(self.surface,(x or sca.x,y or sca.y))
        #self.set_position(Vector2(self.position.x,self.position.y),TopLeft=True)

    def set_rect(self,coord:Vector2):
        self.rect = self.surface.get_rect(topleft=(coord.x,coord.y))

    def on_enter(self,func):
        """
        Ce décorateur crée une fonction qui ajoute celle ci à la liste des fonctions.
        La fonction passé en décoration n'est executé que si la touche Enter est pressé.
        """
        def wrap(_event,*args, **kwargs):
            if _event.type==KEYDOWN:
                if self.isactive and self.active and _event.key == K_RETURN:
                    return func(*args,**kwargs)
        setattr(self,"Enter_func",wrap)
        return True

    def Handle(self, event:py.event.Event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): # If the user clicked on the input_box rect.
                # Toggle the active variable.
                self.active = not self.active
                self.text_color = self.text_color_active if self.active else self.text_color_inactive
            else:
                self.active = False
                self.text_color = self.text_color_inactive
        if self.active:
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
            if event.type == TEXTINPUT:
                    if len(self.text)<self.max_char:
                        self.text += event.text
        self.Enter_func(event)

    def draw(self,ecran):
        render = self.surface.copy()
        
        self.txt_surface = self.FONT.render(self.text or self.paceHolder, True, self.text_color)

        # calcul positions
        x = int(render.get_width()*0.05)
        y = int(render.get_height()//2 - self.txt_surface.get_height()//2)
        # Blit the text.
        render.blit(self.txt_surface,(x,y))
        if time() % 1 > 0.5 and self.active:
            cursor = Rect(self.txt_surface.get_rect(topleft=(x,y-5)).topright, (3, self.txt_surface.get_rect().height))
            py.draw.rect(render, self.text_color, cursor)
        if self.isactive:
            ecran.blit(render,(self.position.x,self.position.y))

    def Update(self): ...

    def Enter_func(self,_event): ...

class Menu:
    """
    classe principale du Menu
    """
    def __init__(self,name,parent=None,childs=None,background=None):
        self.name:str = name
        self.parent:str = parent
        self.childs:list[str] = childs
        self.buttons:list[Button] = []
        _window.menus.append(self)
        if _window == None:
            raise RuntimeError("Vous devez d'abors initialiser la fenêtre")
        if background!=None:
            try:
                self.background = py.image.load(background).convert() # tuile pour le background
                self.background = py.transform.scale(self.background, (_window.screen.get_width(), _window.screen.get_height()))
            except FileNotFoundError:
                print("Your background doesn't seems to exist") 
        else:
            self.background = None

    def add_button(self,func):
        """
        decorateur qui ajoute automatiquement le retour de la fonction à la liste
        """
        _button = func()
        if type(_button)==Button or type(_button)==InputBox:
            self.buttons.append(_button)
        else:
            raise TypeError("You must return a button to add, type returned was :",type(_button))
    
    def Update(self):
        """
        fonction update des bouton du menu avec en premier les event, ensuite les function effectué chaque frame et finalement l'affichage
        """
        for _event in py.event.get():
            if py.QUIT==_event.type:
                _window.destroy()
            for button in self.buttons:
                button.Handle(_event)
        for button in self.buttons:
            button.Update()
        self.Draw(_window.screen)
        
    def Draw(self,ecran:py.Surface):
        """
        fonction pour ajouter chaque bouton à l'écran
        """
        surface = py.Surface((ecran.get_width(),ecran.get_height())).convert_alpha()
        for button in self.buttons:
            button.draw(surface)
        ecran.blit(surface,(0,0))
    
    def get_childs(self):
        """
        fonction pour récupérer les menus enfants
        """
        for _menu in _window.menus:
            if _menu.name in self.childs:
                yield _menu

    def get_child(self,child_name):
        """
        fonction pour récupérer un menu enfants nomé
        """
        for _menu in _window.menus:
            if _menu.name in self.childs and _menu.name == child_name:
                return _menu
        else:
            raise Exception("Menu not found")

    def get_parent(self):
        """
        fonction pour récupérer le menu parent
        """
        for _menu in _window.menus:
            if _menu.name == self.parent:
                return _menu

    def get_button(self,name):
        for button in self.buttons:
            if button.name == name:
                return button