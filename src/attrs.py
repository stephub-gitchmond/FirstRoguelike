import rlmsglog
import rlplayer
from libtcod import libtcodpy as ltc


class Attr(object):
    def __init__(self, owner):
        self.owner = owner


class Fighter(Attr):
    """ Melee-combat related properties and methods """

    def __init__(self, max_hp, defence, power, hp=None, owner=None, death_func=None):
        Attr.__init__(self, owner)
        self.owner = owner
        self.max_hp = max_hp
        self.hp = max_hp if hp is None else hp
        self.defence = defence
        self.power = power
        self.death_func = death_func

    def take_damage(self, damage, leveldata):
        """ Called when this object is dealt damage """
        if damage > 0:
            self.hp -= damage
        if self.hp <= 0 and self.death_func:
            self.death_func(self.owner, leveldata)

    def attack(self, target, leveldata):
        """ Called when this object attempts to deal damage to something """
        if target.fighter:
            f = target.fighter
            damage = self.power - f.defence
            if damage > 0:
                rlmsglog.m(self.owner.name + ' attacks ' + target.name + ' for ' + str(damage) + ' damage')
                f.take_damage(damage, leveldata)
            else:
                rlmsglog.m(self.owner.name + ' attacks ' + target.name + ' but does no damage')

    def is_alive(self):
        return self.hp > 0


class AI(Attr):
    def __init__(self, owner=None):
        Attr.__init__(self, owner)

    def take_turn(self, leveldata):
        pass


class BasicMonsterAI(AI):
    """ AI for a basic monster """

    def __init__(self, owner=None):
        AI.__init__(self, owner)

    def get_move_towards(self, target_x, target_y):
        dx = target_x - self.owner.x
        dy = target_y - self.owner.y
        if abs(dx) > abs(dy):
            dx = 1 if dx > 0 else -1
            dy = 0
        else:
            dx = 0
            dy = 1 if dy > 0 else -1
        return dx, dy

    def take_turn(self, leveldata):
        owner = self.owner

        # monsters only move if the player can see them
        if leveldata.is_visible(owner.x, owner.y):
            px = leveldata.player.x
            py = leveldata.player.y
            dx, dy = self.get_move_towards(px, py)
            new_x = owner.x + dx
            new_y = owner.y + dy
            # if monster would move into player, attack instead
            if new_x == px and new_y == py:
                owner.fighter.attack(leveldata.player, leveldata)
            elif leveldata.is_passable(new_x, new_y):
                owner.x = new_x
                owner.y = new_y


class PlayerAI(AI):
    def __init__(self):
        AI.__init__(self)

    def take_turn(self, leveldata):
        rlplayer.handle_player_action(self.owner, leveldata)


class Item(object):
    """ Represents an item that can be picked up by the player """

    def __init__(self):
        pass


class Inventory(object):
    def __init__(self):
        self.itemlist = []

    def add_item(self, obj):
        """ Add and rlutils.Object to this inventory.
        Returns success flag and message """
        if not obj.item:
            return False, ''
        if len(self.itemlist) >= 26:
            return False, 'Inventory full!'
        self.itemlist.append(obj)
        return True, ''


class Fg(Attr):
    def char(self):
        return None

    def col(self):
        return None


class BasicFg(Fg):
    def __init__(self, char, col, owner=None):
        super(BasicFg, self).__init__(owner)
        self._char = char
        self._col = col

    def char(self):
        return self._char

    def col(self):
        return self._col


class Bg(Attr):
    def col(self):
        return None

    def flag(self):
        return ltc.BKGND_DEFAULT


class WoundIndicatorBg(Bg):
    """ Turns the background increasingly red as the mob is injured """

    def __init__(self, owner=None):
        super(WoundIndicatorBg, self).__init__(owner)

    def col(self):
        if not self.owner.fighter:
            return None
        return ltc.red

    def flag(self):
        if not self.owner.fighter:
            return ltc.BKGND_NONE

        if self.owner.fighter.hp == self.owner.fighter.max_hp:
            # full hp, do not show background
            flag = ltc.BKGND_NONE
        elif self.owner.fighter.hp == 0:
            # no hp, full opacity
            flag = ltc.BKGND_SET
        else:
            # opacity depends on hp
            health = self.owner.fighter.hp / float(self.owner.fighter.max_hp)
            flag = ltc.BKGND_ALPHA(1 - health)

        return flag
