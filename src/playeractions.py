# TODO: not currently used


class Action(object):
    def __init__(self, actor):
        self.actor = actor

    def key(self):
        return None

    def is_valid(self, leveldata):
        return False

    def invoke(self, leveldata):
        pass


class MoveOrAttack(Action):
    def __init__(self, actor, leveldata, dx, dy):
        super(MoveOrAttack, self).__init__(actor)

        # target coords
        self.tx = self.actor.x + dx
        self.ty = self.actor.y + dy

        # get an attackable object on target tile
        objs = leveldata.get_objects(self.tx, self.ty)
        attackables = [o for o in objs if o.fighter]

        if len(attackables) > 0 and self.actor.fighter:
            self.action = 'attack'
            self.target = attackables[0]
        elif leveldata.is_passable(self.tx, self.ty):
            self.action = 'move'
        else:
            self.action = None

    def is_valid(self, leveldata):
        return self.action

    def invoke(self, leveldata):
        if self.action == 'attack':
            self.actor.fighter.attack(self.target)
        elif self.action == 'move':
            self.actor.x = self.tx
            self.actor.y = self.ty
