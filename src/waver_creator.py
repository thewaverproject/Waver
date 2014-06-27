#!/usr/bin/python2.7
# -*- coding: utf-8

import argparse
import md5
import utils.tree.pieces as P
import modules.waver as W

"""
L'objectif de ce script est de creer le fichier .waver relatif a un fichier ou
a un dossier.

Il ne prend qu'un argument : le chemin du dossier/fichier que vous voulez inclure
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Chemin du fichier/dossier')
    parser.add_argument('-o', '--output', help='Nom du fichier de sortie sans l\'extension')
    parser.add_argument('-t', '-tracker', help='Un fichier contenant l\'addresse ips de serveurs trackers.')
    args = parser.parse_args()

    if args.path is None:
        print "Le chemin c'est le minimum"

    pieces_sz = 512 * 1024 * 1024
    pieces, _ = P.path2PiecesTree(args.path, pieces_sz)
    properties = [('port', 5000), ("max_peers", 100), ("pieces_sz", pieces_sz)]
    trackers = ["127.0.0.1"]

    waver_file = W.Waver(pieces, properties, trackers, pieces_sz)
    tmp = waver_file.__str__()
    md5hash = md5.md5(tmp).hexdigest()

    with open(args.output + ".waver", "w") as out_file:
       out_file.write(md5hash + '\n' + tmp)
