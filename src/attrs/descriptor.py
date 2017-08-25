from attrs import *


class Descriptor(Attr):
    def describe(self, owner):
        raise NotImplemented()
