class Inventory(object):
    def __init__(self):
        self.itemlist = []

    def has(self, obj):
        return obj in self.itemlist

    def add(self, obj):
        """ Add and rlutils.Object to this inventory.
        Returns success flag and message """
        if not obj.carryable:
            return False, "Can't pick up " + obj.name
        if len(self.itemlist) >= 26:
            return False, '$orange$Inventory full!$stop$'
        self.itemlist.append(obj)
        return True, 'Picked up ' + obj.name

    def remove(self, obj):
        if self.has(obj):
            self.itemlist.remove(obj)
