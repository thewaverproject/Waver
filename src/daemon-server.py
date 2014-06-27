#!/usr/bin/python2.7
# -*- coding: utf-8

import modules.scheduler as S
import modules.file as F
import modules.waver as W
import argparse as AP

HOST = "127.0.0.1"
PORT = 4200

if __name__ == '__main__':
   # parser les arguments du main
   parser = AP.ArgumentParser()
   parser.add_argument('-f', '--file', help='Le fichier .waver')
   parser.add_argument('-d', '--dir', help='Le dossier de destination du telechargement')
   args = parser.parse_args()

   with open(args.file, 'r') as f:
       s = f.read()
       w = W.file2waver(s)

   f = F.File(args.dir, w)

   S = S.Scheduler(f, HOST, PORT)
   S.start()
