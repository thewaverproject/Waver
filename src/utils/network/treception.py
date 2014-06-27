#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import utils.network.reception as R
import utils.network.emission as E
import threading as T
import socket as S
import sys
import ast


def str2tuple(c):
    res = (c.split(":")[2], c.split(":")[3])
    return res


class TReception(T.Thread):
    def __init__(self, sock_tracker, sock_server, threads, cartographie, file):
        T.Thread.__init__(self)
        self.sock_tracker = sock_tracker
        self.threads = threads
        self.cartographie = cartographie

        # ip_clients = [(ip, port), ...]
        peers = ast.literal_eval(self.sock_tracker.recv(5 * 1024))
        for peer in peers:
            try:
                sock_peer = S.connect((peer[0], peer[1]))
            except S.error:
                sys.exit()
            sock_peer.send(':getinfo')
            self.cartographie.append((peer[0], sock_peer.recv(5 * 1024).split(':')))
            rec = R.Reception(sock_server, file)
            emi = E.Emission(sock_peer, file)
            rec.start()
            emi.start()

            self.threads[peer] = (rec, emi)

    def run(self):
        while 1:
            msgS = self.sock_tracker.recv(1024)
            if msgS.upper() == "FIN" or msgS == "":
                break
            elif msgS[0] == "a":    # ajout dans les dico
                nom = msgS.split(":")[1]
                address[nom] = str2tuple(msgS)
            elif msgS[0] == "s":    # suppression dans le dico
                nom = msgS.split(":")[1]
                del address[nom]
        print msgS, "\n", address, "\n"
        print "Client arrêté. Connexion interrompue."
        self.sock_tracker.close()
