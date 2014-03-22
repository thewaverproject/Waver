#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

class Arborescence:
    def __init__(self, content=None):
        self.content = content
        self.sons = []

    def add_son(self, son):
        self.sons.append(son)

    def define_content(self, content):
        self.content = content

    def delete(self):
        for son in self.sons:
            son.delete()
        self.fils = []
        self.content = None
    """
       Definition des fonction speciales
    """


    def pretty_print(self, depth=1,prefix='-'):
        ret = self.content.__str__()
        for son in self.sons:
            ret += '\n' + prefix*depth + son.pretty_print(depth + 1,prefix)
        return ret

    def __str__(self):
        return self.pretty_print()
