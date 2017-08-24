from libtcod import libtcodpy as ltc


def draw_bar(con, x, y, total_width, name, value, maximum, bar_color, back_color):
    # render a bar (HP, experience, etc). First calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    ltc.console_set_default_background(con, back_color)
    ltc.console_rect(con, x, y, total_width, 1, False, ltc.BKGND_SCREEN)

    # now render the bar on top
    ltc.console_set_default_background(con, bar_color)
    if bar_width > 0:
        ltc.console_rect(con, x, y, bar_width, 1, False, ltc.BKGND_SCREEN)

    # now, centered text with values
    text = name + ':' + str(value) + '/' + str(maximum)
    ltc.console_set_default_foreground(con, ltc.white)
    ltc.console_print_ex(con, x + total_width / 2, y, ltc.BKGND_NONE, ltc.CENTER, text)


def draw_panel_border(con, w, h):
    ltc.console_set_default_foreground(con, ltc.white)
    ltc.console_put_char(con, 0, 0, ltc.CHAR_RADIO_UNSET)
    ltc.console_put_char(con, w - 1, 0, ltc.CHAR_RADIO_UNSET)
    ltc.console_put_char(con, 0, h - 1, ltc.CHAR_RADIO_UNSET)
    ltc.console_put_char(con, w - 1, h - 1, ltc.CHAR_RADIO_UNSET)
    for x in xrange(w - 2):
        ltc.console_put_char(con, x + 1, 0, ltc.CHAR_DHLINE)
        ltc.console_put_char(con, x + 1, h - 1, ltc.CHAR_DHLINE)
    for y in xrange(h - 2):
        ltc.console_put_char(con, 0, y + 1, ltc.CHAR_DVLINE)
        ltc.console_put_char(con, w - 1, y + 1, ltc.CHAR_DVLINE)


def get_names_at_loc(leveldata, x, y):
    objs = leveldata.get_objects_at(x, y)
    return ', '.join(o.name for o in objs).capitalize()


def draw_menu(con, header, options, w, screen_w, screen_h):
    if len(options) > 26:
        raise ValueError('Menu "' + header + '" has ' + str(len(options)) + ' options but max is 26')

    # calculate height (header is word-wrapped)
    header_h = ltc.console_get_height_rect(con, 0, 0, w, screen_h, header)
    h = len(options) + header_h

    # add space for border
    w += 2
    h += 2

    # create new console window
    window = ltc.console_new(w, h)

    # draw border and header
    draw_panel_border(window, w, h)
    ltc.console_set_default_foreground(con, ltc.white)
    ltc.console_print_rect_ex(window, 1, 1, w - 2, h - 2, ltc.BKGND_NONE, ltc.LEFT, header)

    # draw options
    y = header_h + 1
    letter_index = ord('a')
    for o in options:
        text = '(' + chr(letter_index) + ') ' + o
        ltc.console_print_ex(window, 1, y, ltc.BKGND_NONE, ltc.LEFT, text)
        y += 1
        letter_index += 1

    # blit menu to main console
    x = screen_w / 2 - w / 2
    y = screen_h / 2 - h / 2
    ltc.console_blit(window, 0, 0, w, h, 0, x, y, 1.0, 0.7)

    # show menu and wait for player choice
    ltc.console_flush()
    key = ltc.console_wait_for_keypress(True)


def draw_inventory_menu(con, player, w, screen_w, screen_h):
    options = [item.name for item in player.inventory.itemlist]
    header = 'Inventory:' if len(options) > 0 else 'Inventory is empty'

    draw_menu(con, header, options, w, screen_w, screen_h)
