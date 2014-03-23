#!/usr/bin/python2.7
# -*- coding: utf-8 -*-


import utils.tree.arborescence as A


class PiecesTree(A.Arborescence):

    def __init__(self, contents=None):
        A.Arborescence.__init__(self, contents)

    def pretty_print(self, depth=0, prefix='-'):
        if type(self.contents) == str:
            ret = depth * prefix + self.contents
        elif type(self.contents) == tuple:           # (Name, idx_st, idx_end)
            name, idx_st, idx_end = self.contents
            ret = depth * prefix \
                + name + " | " + str(idx_st) + " | " + str(idx_end)
        for s in self.sons:
            ret += "\n" + s.pretty_print(depth + 1, prefix)
        return ret


def depth(s, prefix):
    i, sz = 0, len(s)
    while i < sz and s[i] == prefix:
        i += 1
    return i


def get_contents(line):
    try:
        name = line[0].strip()
    except:
        print ("Nom manquant.")
    try:
        idx_st = int(line[1])
        idx_end = int(line[2])
        contents = name, idx_st, idx_end
    except:
        contents = name
    return contents


def get_line(lines):
    for line in lines:
        yield line


def get_characteristics(line, prefix):
    d = depth(line, prefix)
    contents = get_contents(line[d:].split('|'))
    return (contents, d)


def add_in_tree(tree, contents, d):
    if tree is None:
        tree = PiecesTree(contents)
    else:
        sz = len(tree.sons)
        if d is not 0:
            if sz is 0:
                tree = tree.add_son(PiecesTree(contents))
            else:
                add_in_tree(tree.sons[sz - 1], contents, d - 1)
        else:
            tree.add_son(PiecesTree(contents))
    return tree


def str2PiecesTree(string, prefix='-'):
    res = None
    lines = get_line(string.split('\n'))
    for line in lines:
        contents, d = get_characteristics(line, prefix)
        res = add_in_tree(res, contents, d - 1)
    return res
