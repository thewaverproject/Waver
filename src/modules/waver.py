#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import md5
import utils.tree.pieces as P

class BadFile(Exception):
    pass

class Waver:
    def __init__(self, pieces, properties, tracker, pieces_sz):
        self.pieces = pieces
        self.properties = properties
        self.tracker = tracker
        self.hashes = pieces.extract_hashes()
        self.nb_pieces = self.hashes
        self.pieces_sz = pieces_sz

    def __str__(self):
        ret = "\n"

        ret += ":begin properties\n"
        for const, value in self.properties:
            ret += str(const) + '=' + str(value) + '\n'
        ret += ":end properties\n"

        ret += "\n:begin tracker\n"
        for ip in self.tracker:
            ret += str(ip) + '\n'
        ret += ":end tracker\n"

        ret += "\n:begin pieces\n"
        ret += self.pieces.pretty_print() + '\n'
        ret += ":end pieces\n"

        ret += "\n:begin hash\n"
        for md5hash in self.hashes:
            ret += str(md5hash) + '\n'
        ret += ":end hash"

        return ret

def get_properties(lines,idx):
    i = idx
    prop = []
    while lines[i] != ":begin properties":
        i += 1
    i += 1
    while lines[i] != ":end properties":
        tmp = lines[i].split('=')
        prop.append((tmp[0], tmp[1]))
        i += 1
    return prop , i

def get_tracker(lines,idx):
    i = idx
    tracker = []
    while lines[i] != ":begin tracker":
        i += 1
    i += 1
    while lines[i] != ":end tracker":
        tracker.append(lines[i])
        i += 1
    return tracker , i

def get_pieces(lines,idx):
    str = ''
    i = idx
    magic = 0
    while lines[i] !=  ":begin pieces":
        i += 1
    i += 1
    magic = i
    while lines[i] != ":end pieces":
        if i == magic:
            str += lines[i]
        else:
            str += '\n' + lines[i]
        i += 1
    tree = P.str2PiecesTree(str)
    return tree , i

def get_hash(lines,idx):
    i = idx
    hash = []
    while lines[i] != ":begin hash":
        i += 1
    i += 1
    while lines[i] != ":end hash":
        hash.append(lines[i])
        i += 1
    return hash , i



def file2waver(str):
    lines = str.split('\n')
    if md5.md5('\n'.join(lines[1:])).hexdigest == lines[0:]:
        prop, i = get_properties(str,0)
        tracker, i = get_tracker(str,i)
        pieces, i = get_pieces(str,i)
        hash, i = get_hash(str,i)
        for elt in prop:
            const , value = elt
            if const == "pieces_sz":
                pieces_sz = value
        return Waver(pieces,prop,tracker,pieces_sz)
    else:
        raise BadFile
