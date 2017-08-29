from libtcod import libtcodpy as ltc


class Object(object):
    """ Any object that can exist in the map """

    def __init__(self,
                 name,
                 x, y,
                 fg, bg=None,
                 blocks=True):

        self.name = name
        self.x = x
        self.y = y

        # does this object block others from occupying the same space?
        self.blocks = blocks

        # ATTRIBUTES
        # Each object is just a bag of attributes.
        # Define every possible attribute here, and set to None.
        #
        # Pros: - this acts as a master list
        #       - PyCharm hinting detects it and enable autocomplete
        #
        # Cons: - waste of memory

        # visual attributes
        self.fg = fg
        self.bg = bg
        self.descriptor = None

        # actor attributes
        self.fighter = None
        self.ai = None
        self.inventory = None

        # item attributes
        self.carryable = None
        self.usable = None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, con):
        char = ''
        bg_flag = ltc.BKGND_NONE

        if self.fg:
            char = self.fg.char(self)
            ltc.console_set_default_foreground(con, self.fg.col(self))

        if self.bg:
            bg_flag = self.bg.flag(self)
            ltc.console_set_default_background(con, self.bg.col(self))

        ltc.console_put_char(con, self.x, self.y, char, bg_flag)

    def take_turn(self, leveldata):
        if self.ai:
            self.ai.take_turn(self, leveldata)

    def description(self):
        return self.descriptor.describe(self) if self.descriptor else self.name
