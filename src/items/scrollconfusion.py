from src import rlutils
from src.attrs import ai
from src.attrs.carryable import Carryable
from src.attrs.fg import BasicFg
from src.attrs.usable import Usable
from src.libtcod import libtcodpy as ltc
from src.rlmsglog import m
from src.rlutils import Object


def create(x, y):
    hp = Object('Scroll of confusion',
                x, y,
                BasicFg('?', ltc.dark_blue),
                blocks=False)
    hp.usable = ConfuseItem(5)
    hp.carryable = Carryable()
    return hp


class ConfuseItem(Usable):
    def __init__(self, dist):
        super(ConfuseItem, self).__init__()
        self.dist = dist

    def use(self, owner, leveldata, user):
        target, dist_sq = rlutils.closest_hostile(leveldata.player, leveldata, leveldata.fov_map)

        if not target or dist_sq > self.dist ** 2:
            m("There is no hostile target within range")
            return

        if not target.fighter:
            m("A lightning bolt strikes forth, but has no effect")
            return

        ai.TempAI(ConfusedAi(), duration=5, finishfunc=unconfuse).add_to(target)

        if user.inventory:
            user.inventory.remove(owner)

        m("The " + target.description() + " became confused!")


class ConfusedAi(ai.AI):
    """  AI that moves in a random direction each turn """

    def __init__(self):
        ai.AI.__init__(self)

    def take_turn(self, owner, leveldata):
        # if owner is movable, move in a random direction
        if owner.movable and owner.movable.selfmover():
            # first get all moves
            moves = [(owner.x + 1, owner.y),
                     (owner.x - 1, owner.y),
                     (owner.x, owner.y + 1),
                     (owner.x, owner.y - 1)]

            # filter for possible moves
            moves = [move for move in moves if leveldata.is_passable(move[0], move[1])]

            if not moves:
                return

            # choose random
            move = moves[ltc.random_get_int(0, 0, len(moves)-1)]
            owner.x = move[0]
            owner.y = move[1]


def unconfuse(obj, leveldata):
    """ Call when an object stops being confused """
    m("The " + obj.description() + " regained its wits")
