#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import os.path
import utils.tree.arborescence as A


class PiecesTree(A.Arborescence):

    def __init__(self, contents=None):
        A.Arborescence.__init__(self, contents)

    def pretty_print(self, depth=0, prefix='-'):
        ret = None
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


def path2PiecesTree(path, pieces_sz, nb_pieces=0):
    res = None
    if os.path.isfile(path):
        idx_st = nb_pieces
        idx_end = idx_st + os.path.getsize(path) / pieces_sz
        nb_pieces = idx_end
        res = PiecesTree((os.path.basename(path), idx_st, idx_end))
    elif os.path.isdir(path):
        res = PiecesTree(os.path.basename(path))
        els = os.listdir(path)

        dir_contents = (filter(lambda x: os.path.isdir(path + '/' + x), els)
                     + filter(lambda x: os.path.isfile(path + '/' + x), els))

        for el in dir_contents:
            path_el = path + '/' + el
            if os.path.isdir(path_el):
                tmp, nb_pieces = path2PiecesTree(path_el, pieces_sz, nb_pieces)
                res.add_son(tmp)
            elif os.path.isfile(path_el):
                idx_st = nb_pieces + 1
                idx_end = idx_st + os.path.getsize(path_el) / pieces_sz
                nb_pieces = idx_end
                res.add_son(PiecesTree((el, idx_st, idx_end)))
    return res, nb_pieces
