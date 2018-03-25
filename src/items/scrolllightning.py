from src import rlutils
from src.attrs.carryable import Carryable
from src.attrs.fg import BasicFg
from src.attrs.usable import Usable
from src.libtcod import libtcodpy as ltc
from src.rlmsglog import m
from src.rlutils import Object


def create(x, y):
    hp = Object('Scroll of lightning bolt',
                x, y,
                BasicFg('Z', ltc.dark_blue),
                blocks=False)
    hp.usable = LightningItem(12, 5)
    hp.carryable = Carryable()
    return hp


class LightningItem(Usable):
    def __init__(self, damage, dist):
        super(LightningItem, self).__init__()
        self.damage = damage
        self.dist = dist

    def use(self, owner, leveldata, user):
        target, dist_sq = rlutils.closest_hostile(leveldata.player, leveldata, leveldata.fov_map)

        if not target or dist_sq > self.dist ** 2:
            m("There is no hostile target within range")
            return

        if not target.fighter:
            m("$blue$A lightning bolt strikes forth, but has no effect$stop$")
            return

        target.fighter.take_damage(target, self.damage, leveldata)

        if user.inventory:
            user.inventory.remove(owner)

        m("$blue$A lightning bolt strikes forth,$stop$")
        m("$blue$dealing " + str(self.damage) + " damage to the " + target.name + "!$stop$")
