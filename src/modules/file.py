#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import md5

class File:
    def __init__(self, abspath, waver):
        self.abspath = abspath
        self.waver = waver
        self.state = None

    def read_pieces(self, idx):
        pieces = ""
        path, idx_rel = self.waver.pieces.at(idx)
        with open(self.abspath + path) as f:
            f.seek(idx_rel * self.waver.pieces_sz)
            pieces = f.read(self.waver.pieces_sz)
        return pieces

    def write_pieces(self, string, idx):
        if md5.md5(string).hexdigest() == self.waver.hashes[idx - 1]:
            with open(self.abspath + path) as f:
                f.seek(idx_rel * self.waver.pieces_sz)
                pieces = f.write(string)
        else:
            #throw Exception BadPieces



    def update():
        pass
