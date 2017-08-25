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
