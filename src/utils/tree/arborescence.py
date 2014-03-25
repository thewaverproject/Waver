#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

class Arborescence:
    def __init__(self, contents=None):
        self.contents = contents
        self.sons = []

    def add_son(self, son):
        self.sons.append(son)
        return self

    def define_contents(self, contents):
        self.contents = contents

    def delete(self):
        for son in self.sons:
            son.delete()
        self.fils = []
        self.contents = None
    """
       Definition des fonction speciales
    """


    def pretty_print(self, depth=1,prefix='-'):
        ret = self.contents.__str__()
        for son in self.sons:
            ret += '\n' + prefix*depth + son.pretty_print(depth + 1,prefix)
        return ret

    def __str__(self):
        return self.pretty_print()
