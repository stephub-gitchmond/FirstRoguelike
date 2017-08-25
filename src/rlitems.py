import rlutils
from attrs.carryable import *
from attrs.fg import *
from attrs.usable import *
from libtcod import libtcodpy as ltc

MAX_ROOM_ITEMS = 2


def create_healing_potion(x, y):
    hp = rlutils.Object('Healing Potion',
                        x, y,
                        BasicFg('!', ltc.violet),
                        blocks=False)
    hp.usable = HealingPotion()
    hp.carryable = Carryable()
    return hp


def populate_items(leveldata):
    for room in leveldata.rooms:
        for i in range(ltc.random_get_int(0, 0, MAX_ROOM_ITEMS)):
            x = ltc.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = ltc.random_get_int(0, room.y1 + 1, room.y2 - 1)
            if leveldata.is_passable(x, y):
                item = create_healing_potion(x, y)
                leveldata.objects.append(item)
