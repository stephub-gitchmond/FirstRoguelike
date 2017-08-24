import rlutils
import attrs
from libtcod import libtcodpy as ltc

MAX_ROOM_ITEMS = 2


def create_healing_potion(x, y):
    hp = rlutils.Object('Healing Potion',
                        x, y,
                        attrs.BasicFg('!', ltc.violet),
                        blocks=False)
    hp.item = hp.owns(attrs.Item())
    return hp


def populate_items(leveldata):
    for room in leveldata.rooms:
        for i in range(ltc.random_get_int(0, 0, MAX_ROOM_ITEMS)):
            x = ltc.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = ltc.random_get_int(0, room.y1 + 1, room.y2 - 1)
            if leveldata.is_passable(x, y):
                item = create_healing_potion(x, y)
                leveldata.objects.append(item)
