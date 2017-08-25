from src.attrs.attrs import Attr
from src.libtcod import libtcodpy as ltc


class Bg(Attr):
    def col(self, owner):
        return None

    def flag(self, owner):
        return ltc.BKGND_DEFAULT


class WoundIndicatorBg(Bg):
    """ Turns the background increasingly red as the mob is injured """

    def __init__(self):
        super(WoundIndicatorBg, self).__init__()

    def col(self, owner):
        if not owner.fighter:
            return None
        return ltc.red

    def flag(self, owner):
        if not owner.fighter:
            return ltc.BKGND_NONE

        if owner.fighter.hp == owner.fighter.max_hp:
            # full hp, do not show background
            flag = ltc.BKGND_NONE
        elif owner.fighter.hp == 0:
            # no hp, full opacity
            flag = ltc.BKGND_SET
        else:
            # opacity depends on hp
            health = owner.fighter.hp / float(owner.fighter.max_hp)
            flag = ltc.BKGND_ALPHA(1 - health)

        return flag
