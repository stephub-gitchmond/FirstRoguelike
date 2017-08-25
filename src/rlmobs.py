import rlutils
from attrs.ai import *
from attrs.bg import *
from attrs.fg import *
from attrs.fighter import *

MAX_ROOM_ENEMIES = 3

# use a single copy of stateless attributes
basic_monster_ai = BasicMonsterAI()
wound_indicator_bg = WoundIndicatorBg()


def create_goblin(x, y):
    g = rlutils.Object('Goblin',
                       x, y,
                       BasicFg('g', ltc.dark_green),
                       wound_indicator_bg)
    g.fighter = Fighter(max_hp=10, defence=0, power=3, death_func=mob_death)
    g.ai = basic_monster_ai
    return g


def create_troll(x, y):
    t = rlutils.Object('Troll',
                       x, y,
                       BasicFg('T', ltc.dark_green),
                       wound_indicator_bg)
    t.fighter = Fighter(max_hp=16, defence=1, power=4, death_func=mob_death)
    t.ai = basic_monster_ai
    return t


def create_corpse(mob):
    return rlutils.Object(mob.name + ' corpse',
                          mob.x, mob.y,
                          BasicFg('%', ltc.dark_red),
                          blocks=False)


def mob_death(mob, leveldata):
    """ Removes mob from game and replaces it with a corpse """
    if mob in leveldata.objects:
        corpse = create_corpse(mob)
        leveldata.objects.remove(mob)
        leveldata.objects.append(corpse)


def weighted_choice(choices):
    """ Expects a dictionary of choice:weight """
    total = sum(w for c, w in choices.iteritems())
    r = ltc.random_get_int(0, 0, total)
    upto = 0
    for c, w in choices.iteritems():
        upto += w
        if upto >= r:
            return c


def populate_enemies(leveldata):
    """ Takes some LevelData and populates the 'objects' variable
        with some monsters """
    generators = {create_goblin: 80, create_troll: 20}

    for room in leveldata.rooms:
        for n in range(ltc.random_get_int(0, 0, MAX_ROOM_ENEMIES)):
            x = ltc.random_get_int(0, room.x1, room.x2)
            y = ltc.random_get_int(0, room.y1, room.y2)
            if leveldata.is_passable(x, y):
                enemy = weighted_choice(generators)(x, y)
                leveldata.objects.append(enemy)
