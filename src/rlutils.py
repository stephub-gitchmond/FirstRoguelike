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
        self.fg = None if fg is None else self.owns(fg)
        self.bg = None if bg is None else self.owns(bg)
        self.blocks = blocks

        self.owner = None

        self.fighter = None
        self.ai = None
        self.inventory = None
        self.item = None

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, con):

        char = ''
        bg_flag = ltc.BKGND_NONE

        if self.fg:
            char = self.fg.char()
            ltc.console_set_default_foreground(con, self.fg.col())

        if self.bg:
            bg_flag = self.bg.flag()
            ltc.console_set_default_background(con, self.bg.col())

        ltc.console_put_char(con, self.x, self.y, char, bg_flag)

    def take_turn(self, leveldata):
        if self.ai:
            self.ai.take_turn(leveldata)

    def owns(self, child):
        child.owner = self
        return child