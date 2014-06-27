#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import utils.network.temission as TE
import utils.network.treception as TR
import modules.file
import threading as T
import socket as S
import sys
import ast


class Scheduler(T.Thread):
    def __init__(self, file, host, port):
        T.Thread.__init__(self)
        self.file = file
        self.threads = {}
        self.host = host
        self.port = port
        self.cartographie = None
        self.msg = ''
        self.sock_tracker = S.socket(S.AF_INET, S.SOCK_STREAM)
        self.sock_server = S.socket(S.AF_INET, S.SOCK_STREAM)
        self.server = None

        try:
            self.sock_tracker.connect((self.host, self.port))
        except S.error:
            sys.exit()

        semi = TE.TEmission(self.sock_tracker)
        srec = TR.TReception(self.sock_tracker, self.sock_server, self.threads, self.cartographie, self.file)
        semi.start()
        srec.start()
        self.server = (semi, srec)


    def run(self):
        while 1:
            pass
