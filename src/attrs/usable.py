class Usable(object):
    """ Represents an item that can be used by the player """

    def __init__(self):
        pass

    def use(self, owner, leveldata, user):
        """
        Uses the item.
        Returns True if the item was succesfully used, and a message describing what happened """
        return False, "The " + owner.name + "doesn't do anything... yet"


class HealingPotion(Usable):
    def use(self, owner, leveldata, user, target=None):
        if not user.fighter:
            return False, "You can't use a healing potion if you have no health"

        if user.fighter.is_at_max_health():
            return False, "Can't heal, already at full health"

        user.fighter.hp += 15
        remove_from_inv(owner, user)


def remove_from_inv(obj, user):
    if user.inventory and user.inventory.has(obj):
        user.inventory.remove(obj)
