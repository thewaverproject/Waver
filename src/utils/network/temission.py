# -*- coding: utf-8 -*-

import threading as T


class SEmission(T.Thread):
    def __init__(self, sock):
        T.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while 1:
            msgC = raw_input("> ")
            self.sock.send(msgC)
