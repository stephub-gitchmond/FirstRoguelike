import src.rlmsglog as rlmsglog


class Item(object):
    """ Represents an item that can be picked up by the player """

    def __init__(self, usefunction=None):
        self.usefunction = usefunction

    def use(self, owner, leveldata, target=None):
        if not self.usefunction:
            rlmsglog.m(owner.name + " cannot be used")
        self.usefunction(owner, leveldata, target)
