from attrs import *


class Descriptor(Attr):
    def __init__(self, func):
        self.func = func

    def describe(self, owner):
        return self.func(owner)
