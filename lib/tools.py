import inspect

class Vector2:
    """
    class Vecteur 2 dimension pour un stockage des position et range plus facile qu'avec un array tuple
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y

def attr_exist(name,obj):
    """
    vérification que la fonction ne va pas en écraser une autre
    """
    for attr in inspect.getmembers(obj):
        if name in attr[0]:
                print("Function already exist in the class, take another name")
                raise RuntimeError

class ConnRejected(Exception):
    """
    Execption when server reject connection
    """
    def __init__(self, *args: object,**kargs):
        super().__init__(*args,**kargs)