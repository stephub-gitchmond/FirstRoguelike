import os

# necessary because libtcod expects everything to be in working dir
os.chdir('./libtcod')
from libtcod import libtcodpy as ltc

import leveltools
import rlmobs
import rlplayer
import guiutils
import rlmsglog
import rlitems


def handle_input(key, mouse, game_state, leveldata, con):
    # TODO remove con from params
    """ Handles user input. Returns True if the player has taken a turn """

    if key.vk == ltc.KEY_ENTER and key.lalt:
        # alt+enter toggles fullscreen
        ltc.console_set_fullscreen(not ltc.console_is_fullscreen())
        return False

    elif key.vk == ltc.KEY_F4 and key.lalt:
        # exit
        global should_exit
        should_exit = True
        return False

    elif chr(key.c) == 'i':
        guiutils.draw_inventory_menu(con,
                                     leveldata.player,
                                     SCREEN_WIDTH - 30,
                                     SCREEN_WIDTH, SCREEN_HEIGHT)

    elif game_state is GS_PLAYING:
        # otherwise, player takes an action
        return rlplayer.handle_key(key, leveldata.player)


def draw_level(con, leveldata):
    for x, y in leveldata.coords():
        lit = leveldata.is_visible(x, y)
        t = leveldata.level[x][y]  # current tile
        if lit:
            t.explored = True
        if t.explored:
            t.draw(con, x, y, lit)

    delayed = []  # draw blocking objects last so they appear on top
    for obj in leveldata.objects:
        if leveldata.is_visible(obj.x, obj.y):
            if obj.blocks:
                delayed.append(obj)
            else:
                obj.draw(con)
    for obj in delayed:
        obj.draw(con)


def draw_gui(gui_panel, con, leveldata, mouse):
    ltc.console_set_default_background(gui_panel, ltc.black)
    guiutils.draw_bar(gui_panel,
                      2, 2,
                      GUI_BAR_WIDTH,
                      'HP',
                      leveldata.player.fighter.hp, leveldata.player.fighter.max_hp,
                      ltc.light_red, ltc.dark_red)
    guiutils.draw_panel_border(gui_panel, PANEL_WIDTH, PANEL_HEIGHT)
    rlmsglog.msg_log.draw_log(gui_panel, MSG_LOG_X, MSG_LOG_Y, MSG_LOG_W, MSG_LOG_H)

    objs_under_mouse = guiutils.get_names_at_loc(leveldata, mouse.cx, mouse.cy)
    ltc.console_set_default_foreground(con, ltc.white)
    ltc.console_print_ex(con, 0, 0, ltc.BKGND_NONE, ltc.LEFT, objs_under_mouse)


def clear_console(con):
    ltc.console_set_default_background(con, ltc.BKGND_NONE)
    ltc.console_clear(con)


# constants
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

PANEL_WIDTH = SCREEN_WIDTH
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

GUI_BAR_WIDTH = 20

MSG_LOG_X = GUI_BAR_WIDTH + 3
MSG_LOG_Y = 1
MSG_LOG_W = PANEL_WIDTH - MSG_LOG_X - 1
MSG_LOG_H = PANEL_HEIGHT - 2

LEVEL_WIDTH = SCREEN_WIDTH
LEVEL_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT

TORCH_RADIUS = 10

# game states
GS_PLAYING = 'playing'
GS_DEAD = 'dead'

# This flag is true if the game should exit
should_exit = False


def main():
    # setup screen
    ltc.console_set_custom_font('lucida10x10_gs_tc.png', ltc.FONT_TYPE_GREYSCALE | ltc.FONT_LAYOUT_TCOD)
    ltc.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/ltc tutorial', fullscreen=False)
    ltc.sys_set_fps(LIMIT_FPS)

    con = ltc.console_new(LEVEL_WIDTH, LEVEL_HEIGHT)
    gui_panel = ltc.console_new(PANEL_WIDTH, PANEL_HEIGHT)

    # setup level
    leveldata, start_pos = leveltools.make_level(LEVEL_WIDTH, LEVEL_HEIGHT)
    fov_recompute = True

    # setup player
    leveldata.player = rlplayer.create_player(start_pos[0], start_pos[1])
    leveldata.objects.insert(0, leveldata.player)

    rlmobs.populate_enemies(leveldata)
    rlitems.populate_items(leveldata)

    rlmsglog.m('Welcome to the dungeon!')

    # game state
    game_state = GS_PLAYING

    # MAIN LOOP
    while not ltc.console_is_window_closed():

        # get user input
        mouse = ltc.Mouse()
        key = ltc.Key()
        ltc.sys_check_for_event(ltc.EVENT_KEY_PRESS | ltc.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            leveldata.recompute_fov(TORCH_RADIUS)

        # draw level
        draw_level(con, leveldata)
        # noinspection PyTypeChecker
        draw_gui(gui_panel, con, leveldata, mouse)

        # display level
        ltc.console_blit(con, 0, 0, LEVEL_WIDTH, LEVEL_HEIGHT, 0, 0, 0)
        ltc.console_blit(gui_panel, 0, 0, PANEL_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
        ltc.console_flush()
        clear_console(con)
        clear_console(gui_panel)

        # handle user input
        # noinspection PyTypeChecker
        player_taken_turn = handle_input(key, mouse, game_state, leveldata, con)

        if should_exit:
            break

        # all objects take their turn - player is first
        if game_state == GS_PLAYING and player_taken_turn:
            fov_recompute = True
            for o in leveldata.objects:
                o.take_turn(leveldata)

        if not leveldata.player.fighter.is_alive():
            game_state = GS_DEAD


if __name__ == "__main__":
    main()
