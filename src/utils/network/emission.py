#!/usr/bin/python2.7
# -*- coding: utf-8

import threading


class Emission(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn
        self.msg = ''

    def run(self):
        while 1:
            #update self.pending
            if self.msg is not '':
                msg = self.msg
                self.connexion.send(msg)
                self.msg = ''
