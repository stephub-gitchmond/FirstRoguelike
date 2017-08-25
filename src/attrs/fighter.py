import src.rlmsglog as rlmsglog
from src.attrs.attrs import Attr


class Fighter(Attr):
    """ Melee-combat related properties and methods """

    def __init__(self, max_hp, defence, power, hp=None, death_func=None):
        Attr.__init__(self)
        self.max_hp = max_hp
        self.__hp__ = max_hp if hp is None else hp
        self.defence = defence
        self.power = power
        self.death_func = death_func

    @property
    def hp(self):
        return self.__hp__

    @hp.setter
    def hp(self, hp):
        # ensure hp is never set above max, or below zero
        if hp > self.max_hp:
            self.__hp__ = self.max_hp
        elif hp < 0:
            self.__hp__ = 0
        else:
            self.__hp__ = hp

    def take_damage(self, owner, damage, leveldata):
        """ Called when this object is dealt damage """
        if damage > 0:
            self.hp -= damage

        if self.hp == 0 and self.death_func:
            self.death_func(owner, leveldata)

    def attack(self, owner, target, leveldata):
        """ Called when this object attempts to deal damage to something """
        if target.fighter:
            damage = self.power - target.fighter.defence
            if damage > 0:
                rlmsglog.m(owner.name + ' attacks ' + target.name + ' for ' + str(damage) + ' damage')
                target.fighter.take_damage(target, damage, leveldata)
            else:
                rlmsglog.m(owner.name + ' attacks ' + target.name + ' but does no damage')

    def is_alive(self):
        return self.hp > 0

    def is_at_max_health(self):
        return self.hp == self.max_hp
