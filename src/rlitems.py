from items import potionhealing
from items import scrollconfusion
from items import scrolllightning
from libtcod import libtcodpy as ltc

MAX_ROOM_ITEMS = 2


def populate_items(leveldata):
    for room in leveldata.rooms:
        for i in range(ltc.random_get_int(0, 0, MAX_ROOM_ITEMS)):
            x = ltc.random_get_int(0, room.x1 + 1, room.x2 - 1)
            y = ltc.random_get_int(0, room.y1 + 1, room.y2 - 1)
            if leveldata.is_passable(x, y):
                item = random_item(x, y)
                leveldata.objects.append(item)


# weighted drop chances for items
choices = {potionhealing.create: 7,
           scrolllightning.create: 3,
           scrollconfusion.create: 5}


def random_item(x, y):
    total = sum(choices.values())
    r = ltc.random_get_int(0, 0, total)
    upto = 0
    for c, w in choices.iteritems():
        if upto + w >= r:
            return c(x, y)
        upto += w
    assert False, "Failed to pick random item"
