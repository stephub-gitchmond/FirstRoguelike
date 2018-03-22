from attrs import *


class Usable(Attr):
    """ Represents an item that can be used by the player """

    def __init__(self):
        super(Usable, self).__init__()

    def use(self, owner, leveldata, user):
        """
        Uses the item.
        Returns boolean saying if item was successfully used
        and a message describing what happened
        """
        return False, "The " + owner.name + "doesn't do anything... yet"
