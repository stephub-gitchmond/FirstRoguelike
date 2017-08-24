from libtcod import libtcodpy as ltc
import textwrap


class MessageLog:
    """ A list of messages. Can draw those messages to a w*h area of a console. """

    def __init__(self):
        self.msgs = []

    def msg(self, text, colour=ltc.white):
        self.msgs.append((text, colour))

    def draw_log(self, con, x, y, w, h):
        last_msgs = self.msgs[-h:]  # last h messages
        last_lines = [(text, c)
                      for msg, c in last_msgs
                      for text in textwrap.wrap(msg, w)]
        _y = y
        for text, colour in last_lines[-h:]:  # take last h lines
            ltc.console_set_default_foreground(con, colour)
            ltc.console_print_ex(con, x, _y, ltc.BKGND_NONE, ltc.LEFT, text)
            _y += 1

# global message log
msg_log = MessageLog()

# alias function for convenience
# prints a message to the global message log
m = msg_log.msg
