import rlmobs
import rlutils
import rlmsglog
from attrs.ai import *
from attrs.bg import *
from attrs.fg import *
from attrs.fighter import *
from attrs.inventory import *
from libtcod import libtcodpy as ltc

pas = {ltc.KEY_UP: 'PA_UP',
       ltc.KEY_DOWN: 'PA_DOWN',
       ltc.KEY_LEFT: 'PA_LEFT',
       ltc.KEY_RIGHT: 'PA_RIGHT',
       ltc.KEY_SPACE: 'PA_SKIP',
       'g': 'PICK_UP'}

pa = None  # player action


def handle_key(key):
    """ Chooses the player action based on the keypress.
        Returns true if the keypress has been handled """
    global pa
    if key.vk in pas:
        pa = pas[key.vk]
        return True
    if chr(key.c) in pas:
        pa = pas[chr(key.c)]
        return True
    else:
        pa = None
        return False


def handle_player_action(player, leveldata):
    """ Takes action based on the 'pa' flag """
    if pa == 'PA_UP':
        move_or_attack(player, leveldata, 0, -1)
    elif pa == 'PA_DOWN':
        move_or_attack(player, leveldata, 0, 1)
    elif pa == 'PA_LEFT':
        move_or_attack(player, leveldata, -1, 0)
    elif pa == 'PA_RIGHT':
        move_or_attack(player, leveldata, 1, 0)
    elif pa == 'PICK_UP':
        pickup_item(player, leveldata)


def move_or_attack(player, leveldata, dx, dy):
    x = player.x + dx
    y = player.y + dy

    # get an attackable object on target tile
    attackables = [o for o in leveldata.get_objects(x, y) if o.fighter]

    if len(attackables) == 0:
        # move to target
        if leveldata.is_passable(x, y):
            player.x += dx
            player.y += dy
    else:
        # attack target
        player.fighter.attack(player, attackables[0], leveldata)


def pickup_item(player, leveldata):
    if player.inventory is not None:
        objs = leveldata.get_objects_at(player.x, player.y)

        # get objects that have the 'item' attribute
        items = [obj for obj in objs if obj.item]
        if len(items) > 0:
            item = items[0]
            success, msg = player.inventory.add_item(item)

            if success:
                rlmsglog.m('Picked up ' + item.name)
                leveldata.objects.remove(item)
            elif msg:
                rlmsglog.m(msg)


def player_death(player, leveldata):
    rlmobs.mob_death(player, leveldata)


def create_player(x, y):
    p = rlutils.Object('Player',
                       x, y,
                       BasicFg('@', ltc.white),
                       WoundIndicatorBg())
    p.fighter = Fighter(max_hp=30, defence=2, power=5, death_func=player_death)
    p.ai = PlayerAI()
    p.inventory = Inventory()
    return p
