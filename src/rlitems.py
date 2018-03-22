from libtcod import libtcodpy as ltc
from items import healingpotion
from items import lightingscroll

MAX_ROOM_ITEMS = 2


def populate_items(leveldata):
    for room in leveldata.rooms:
        for i in range(ltc.random_get_int(0, 0, MAX_ROOM_ITEMS)):
            x = ltc.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = ltc.random_get_int(0, room.y1 + 1, room.y2 - 1)
            if leveldata.is_passable(x, y):
                item = random_item(x, y)
                leveldata.objects.append(item)


def random_item(x, y):
    dice = ltc.random_get_int(0, 0, 100)
    if dice < 70:
        return healingpotion.create(x, y)
    else:
        return lightingscroll.create(x, y)
