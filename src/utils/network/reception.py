#!/usr/bin/python2.7
# -*- coding: utf-8

import threading
import queue


class Reception(threading.Thread):

    def __init__(self, conn, file, queue):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.file = file

    def run(self):
        while 1:
            type, msg = self.connexion.recv(1024)
            if type == 'piece':
                idx, piece = msg.split(',')
                file.write_pieces(pieces, idx)
            elif type == 'request':
                pass
