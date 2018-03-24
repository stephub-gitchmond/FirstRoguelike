import src.rlplayer
from src.attrs.attrs import Attr

ATTITUDE_HOSTILE = "hostile"
ATTITUDE_FRIENDLY = "friendly"
ATTITUDE_NA = "n/a"


class AI(Attr):
    def __init__(self):
        Attr.__init__(self)

    def take_turn(self, owner, leveldata):
        pass

    def attitude_towards(self, target, leveldata):
        pass


class BasicMonsterAI(AI):
    """ AI for a basic monster """

    def __init__(self):
        AI.__init__(self)

    @staticmethod
    def get_move_towards(owner, target_x, target_y):
        dx = target_x - owner.x
        dy = target_y - owner.y
        if abs(dx) > abs(dy):
            dx = 1 if dx > 0 else -1
            dy = 0
        else:
            dx = 0
            dy = 1 if dy > 0 else -1
        return dx, dy

    def take_turn(self, owner, leveldata):
        # monsters only move if the player can see them
        if leveldata.is_visible(owner.x, owner.y):
            px = leveldata.player.x
            py = leveldata.player.y
            dx, dy = self.get_move_towards(owner, px, py)
            new_x = owner.x + dx
            new_y = owner.y + dy
            # if monster would move into player, attack instead
            if new_x == px and new_y == py:
                owner.fighter.attack(owner, leveldata.player, leveldata)
            elif leveldata.is_passable(new_x, new_y):
                owner.x = new_x
                owner.y = new_y

    def attitude_towards(self, target, leveldata):
        """ Only hostile towards player """
        return ATTITUDE_HOSTILE if target == leveldata.player else ATTITUDE_FRIENDLY


class PlayerAI(AI):
    def __init__(self):
        AI.__init__(self)
        self.action = None

    def take_turn(self, owner, leveldata):
        src.rlplayer.handle_player_action(owner, leveldata)


class TempAI(AI):
    """ This AI handles temporarily replacing an objects AI with a different one, for a specified number of turns. """

    def __init__(self, tempai, duration, finishfunc=None):
        AI.__init__(self)
        self.prevai = None
        self.tempai = tempai
        self.duration = duration
        self.finishfunc = finishfunc

    def add_to(self, newowner):
        """ Call this to add the temporary AI to an object """
        self.prevai = newowner.ai
        newowner.ai = self

    def take_turn(self, owner, leveldata):
        # delegate action to the temporary AI
        self.tempai.take_turn(owner, leveldata)

        # reduce the remaining time by one turn
        self.duration -= 1

        # restore the previous AI if necessary
        if self.duration <= 0:
            owner.ai = self.prevai

            if self.finishfunc:
                self.finishfunc(owner, leveldata)
