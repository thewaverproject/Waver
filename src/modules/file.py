#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import md5
from math import ceil


class BadPiece(Exception):
    pass


class File:

    """
        La variable d'attribut `self.state` est de la forme:
            ((ip, [tableau de 100 cases: chaque case contient l'avancement
                du pair pour le groupement de pieces.)],
             [tableau contenant les identifiants des 100 pieces les plus rares],
             [tableau de boolean representant le telechargement des pieces]
    """

    def __init__(self, abspath, waver):
        self.abspath = abspath
        self.waver = waver
        self.state = None

    def read_piece(self, idx):
        pieces = ""
        path, idx_rel = self.waver.pieces.at(idx)
        with open(self.abspath + path) as f:
            f.seek(idx_rel * self.waver.pieces_sz)
            pieces = f.read(self.waver.pieces_sz)
        return pieces

    def write_piece(self, string, idx):
        if md5.md5(string).hexdigest() == self.waver.hashes[idx - 1]:
            path, idx_rel = self.waver.pieces.at(idx)
            with open(self.abspath + path) as f:
                f.seek(idx_rel * self.waver.pieces_sz)
                f.write(string)
            self.state[2][idx] = True
        else:
            raise BadPiece

    def next_download(self):
        ret = []
        i, j = 0, 0
        _, rarest, pieces = self.state
        while j < 100 and i < 5:
            # La j-eme plus rare est-elle telechargee (true == deja telechargee)
            if pieces[rarest[j]] is False:
                ret += rarest[j]
                i += 1
            j += 1
        j = 0
        while i < 5:
            while j < len(pieces) and pieces[j] is True:
                j += 1
            if j not in ret:
                ret += pieces[j]
            j += 1
        return ret

    def update(self, network_state, rarest):
        self.state = network_state, rarest, self.state[2]

    def is_download(self, idx):
        if self.state[2][idx] is True:
            return 1
        else:
            return 0

    def is_downloadb(self, idx):
        return self.state[2][idx]

    def info(self):
        sz_subdiv = int(ceil(len(self.state[2]) / float(100)))
        ret = []
        for i in range(0, 99):
            sum = 0
            for j in range(0, sz_subdiv - 1):
                sum += self.is_download(100 * i + j)
            ret.append(int(100 * sum / sz_subdiv))
        return ret
