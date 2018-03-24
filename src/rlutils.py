from libtcod import libtcodpy as ltc
from attrs import ai


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
        self.movable = None

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


def distsq(x1, y1, x2, y2):
    return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)


def closest_hostile(subject, leveldata, fov_map=None):
    """ Returns the closest hostile creature, and the square of the distance """

    hostiles = [o for o in leveldata.objects
                if o.ai and o.ai.attitude_towards(subject, leveldata) is ai.ATTITUDE_HOSTILE]

    if fov_map:
        hostiles = [o for o in hostiles if ltc.map_is_in_fov(fov_map, o.x, o.y)]

    min_dist_sq = None
    closest = None

    for h in hostiles:
        dist_sq = distsq(subject.x, subject.y, h.x, h.y)
        if min_dist_sq is None or min_dist_sq > dist_sq:
            min_dist_sq = dist_sq
            closest = h

    return closest, min_dist_sq
