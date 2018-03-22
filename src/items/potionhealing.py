from src.attrs.carryable import Carryable
from src.attrs.descriptor import Descriptor
from src.attrs.fg import BasicFg
from src.attrs.usable import Usable
from src.libtcod import libtcodpy as ltc
from src.rlutils import Object


def create(x, y):
    hp = Object('Healing Potion',
                x, y,
                BasicFg('!', ltc.violet),
                blocks=False)
    hp.usable = Healer(healamount=ltc.random_get_int(0, 5, 15))
    hp.carryable = Carryable()
    hp.descriptor = Descriptor(lambda o: o.name + " +" + str(o.usable.healamount))
    return hp


class Healer(Usable):
    def __init__(self, healamount):
        super(Healer, self).__init__()
        self.healamount = healamount

    def use(self, owner, leveldata, user, target=None):
        if not user.fighter:
            return False, "You can't use a " + owner.name + " if you have no health"

        if user.fighter.is_at_max_health():
            return False, "Can't heal, already at full health"

        user.fighter.hp += self.healamount
        user.inventory.remove(owner)

        return 'True', "$green$Your wounds start to close$stop$"
