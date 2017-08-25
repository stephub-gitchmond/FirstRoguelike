from src.attrs.attrs import Attr


class Fg(Attr):
    def char(self, owner):
        return None

    def col(self, owner):
        return None


class BasicFg(Fg):
    def __init__(self, char, col):
        super(BasicFg, self).__init__()
        self._char = char
        self._col = col

    def char(self, owner):
        return self._char

    def col(self, owner):
        return self._col
