import guiutils
from libtcod import libtcodpy as ltc


class MessageLog(object):
    """ A list of messages. Can draw those messages to a w*h area of a console. """

    def __init__(self):
        self.msgs = []

    def msg(self, text, colour=ltc.white):
        self.msgs.append((text, colour))

    def draw_log(self, con, x, y, w, h):
        last_msgs = self.msgs[-h:]  # last h messages
        for i, (text, colour) in enumerate(last_msgs):
            # the latest message is white, the rest are grey
            col = ltc.white if i == len(last_msgs) - 1 else ltc.grey

            guiutils.dotext(con, x, y + i, text, fg=col)


# global message log
msg_log = MessageLog()

# alias function for convenience
# prints a message to the global message log
m = msg_log.msg
