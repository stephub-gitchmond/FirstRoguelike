import itertools

from libtcod import libtcodpy as ltc

COLOUR_DARK_WALL = ltc.Color(0, 0, 100)
COLOUR_LIGHT_WALL = ltc.Color(80, 70, 30)
COLOUR_DARK_GROUND = ltc.Color(50, 50, 150)
COLOUR_LIGHT_GROUND = ltc.Color(200, 180, 50)

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30


class LevelData:
    """ Big bag of data about the level """

    def __init__(self, w, h, level, rooms, objects=None, player=None):
        self.w = w
        self.h = h
        self.level = level
        self.rooms = rooms
        self.objects = objects if objects else []
        self.player = player

        self.fov_map = ltc.map_new(w, h)
        self.create_fov_map()

    def is_in_map(self, x, y):
        """ Returns True if the given coord is within the bounds of the level """
        return x < len(self.level) and y < len(self.level[x])

    def get_objects(self, x, y):
        """ Returns an iterable of all objects at the given location """
        return filter(lambda o: o.x == x and o.y == y, self.objects)

    def is_passable(self, x, y):
        """ True of the given tile is passable and there is no blocking object """
        if not self.is_in_map(x, y):
            return False

        tile_passable = self.level[x][y].passable

        blocking_object = any(map(lambda o: o.blocks, self.get_objects(x, y)))
        return tile_passable and not blocking_object

    def coords(self):
        """ Returns an iterable of all x,y coords in the map """
        return itertools.product(xrange(self.w), xrange(self.h))

    def create_fov_map(self):
        for x, y in self.coords():
            t = self.level[x][y]
            ltc.map_set_properties(self.fov_map, x, y, t.transparent, t.passable)

    def recompute_fov(self, radius, light_walls=True, fov_algo=0):
        ltc.map_compute_fov(self.fov_map, self.player.x, self.player.y, radius, light_walls, fov_algo)

    def is_visible(self, x, y):
        """ Returns true if the specified location is within the players FOV """
        return ltc.map_is_in_fov(self.fov_map, x, y)

    def get_objects_at(self, x, y):
        """ Returns an iterable of all objects at the given coordinates """
        return filter(lambda o: o.x == x and o.y == y, self.objects)


class Tile:
    def __init__(self, unlit_col_bg, lit_col_bg, passable, transparent=None, char=None, unlit_col_fg=None,
                 lit_col_fg=None, explored=False):
        self.unlit_col_bg = unlit_col_bg
        self.lit_col_bg = lit_col_bg
        self.passable = passable
        self.transparent = passable if transparent is None else transparent
        self.explored = explored

        self.char = char
        self.unlit_col_fg = unlit_col_fg if unlit_col_fg else unlit_col_bg.__mul__(1.3)
        self.lit_col_fg = lit_col_fg if lit_col_fg else lit_col_bg.__mul__(1.3)

    def draw(self, con, x, y, lit=False):
        col_bg = self.lit_col_bg if lit else self.unlit_col_bg
        ltc.console_set_char_background(con, x, y, col_bg, ltc.BKGND_SET)
        if self.char:
            col_fg = self.lit_col_fg if lit else self.unlit_col_fg
            ltc.console_set_default_foreground(con, col_fg)
            ltc.console_put_char(con, x, y, self.char, ltc.BKGND_NONE)


def floor_tile():
    return Tile(COLOUR_DARK_GROUND, COLOUR_LIGHT_GROUND, True, char='.')


def wall_tile():
    return Tile(COLOUR_DARK_WALL, COLOUR_LIGHT_WALL, False, char='#')


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        cx = (self.x1 + self.x2) / 2
        cy = (self.y1 + self.y2) / 2
        return cx, cy

    def intersects(self, other):
        """ returns true if this rectangle intersects with another one """
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(level, rect):
    for x in range(rect.x1, rect.x2 + 1):
        for y in range(rect.y1, rect.y2 + 1):
            level[x][y] = floor_tile()


def create_h_tunnel(level, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        level[x][y] = floor_tile()


def create_v_tunnel(level, x, y1, y2):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        level[x][y] = floor_tile()


def make_level(width, height):
    level = [[wall_tile() for _ in range(height)] for _ in range(width)]
    start_pos = 0, 0
    rooms = []

    for r in range(MAX_ROOMS):
        # random width and height
        w = ltc.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = ltc.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = ltc.random_get_int(0, 0, width - w - 1)
        y = ltc.random_get_int(0, 0, height - h - 1)

        new_room = Rect(x, y, w, h)

        # check if new room intersencts an existing room
        failed = any(map(new_room.intersects, rooms))

        if not failed:
            create_room(level, new_room)
            if len(rooms) == 0:
                # this is the first room
                start_pos = new_room.center()
            else:
                # connect to previous room
                x1, y1 = new_room.center()
                x2, y2 = rooms[-1].center()
                create_h_tunnel(level, x1, x2, y1)
                create_v_tunnel(level, x2, y1, y2)

            rooms.append(new_room)

    return LevelData(width, height, level, rooms), start_pos
