import src.rlmsglog
from src.attrs.attrs import Attr


class Fighter(Attr):
    """ Melee-combat related properties and methods """

    def __init__(self, max_hp, defence, power, hp=None, death_func=None):
        Attr.__init__(self)
        self.max_hp = max_hp
        self.hp = max_hp if hp is None else hp
        self.defence = defence
        self.power = power
        self.death_func = death_func

    def take_damage(self, owner, damage, leveldata):
        """ Called when this object is dealt damage """
        if damage > 0:
            self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        if self.hp == 0 and self.death_func:
            self.death_func(owner, leveldata)

    def attack(self, owner, target, leveldata):
        """ Called when this object attempts to deal damage to something """
        if target.fighter:
            damage = self.power - target.fighter.defence
            if damage > 0:
                src.rlmsglog.m(owner.name + ' attacks ' + target.name + ' for ' + str(damage) + ' damage')
                target.fighter.take_damage(target, damage, leveldata)
            else:
                src.rlmsglog.m(owner.name + ' attacks ' + target.name + ' but does no damage')

    def is_alive(self):
        return self.hp > 0
