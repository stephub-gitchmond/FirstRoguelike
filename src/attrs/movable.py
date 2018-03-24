from attrs import Attr


class Movable(Attr):
    """ Flags that the given object can move """

    def __init__(self):
        Attr.__init__(self)

    def selfmover(self):
        """ Returns True if the object can move under it's own power """
        return False


class MovableCreature(Movable):
    def __init__(self):
        Movable.__init__(self)

    def selfmover(self):
        return True
