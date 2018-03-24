from attrs import *
from src.rlmsglog import m


class Usable(Attr):
    """ Represents an item that can be used by the player """

    def __init__(self):
        super(Usable, self).__init__()

    def use(self, owner, leveldata, user):
        """ Uses the item. """
        m("The " + owner.name + "doesn't do anything... yet")
