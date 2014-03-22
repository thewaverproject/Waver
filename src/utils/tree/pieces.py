#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import utils.tree.arborescence as A

class PiecesTree(A.Arborescence):
    def __init__(self,content=None):
        A.Arborescence.__init__(self, content)

    def pretty_print(self, depth=0, prefix='-'):
        if type(self.content) == str:
            ret = depth * prefix + self.content
        elif type(self.content) == tuple: # (Name, idx_st, idx_end)
            name, idx_st, idx_end = self.content
            ret = depth * prefix + " " + name + " | " + str(idx_st) + " | " + str(idx_end)
        for s in self.sons:
            ret += "\n" + s.pretty_print(depth + 1,prefix)
        return ret
