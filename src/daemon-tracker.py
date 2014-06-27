#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import sqlite3

DB_NAME = 'Torrent.db'

# Hash # Nom # Pairs (date, ip)


def db_create(db_conn, nom):
    query = """
    CREATE TABLE {0}
     (
        ID INTEGER NOT NULL,
        HASH VARCHAR(32) NOT NULL,
        NOM VARCHAR(200) NOT NULL,
        PAIRS VARCHAR(8000) NOT NULL
     )""" % nom

 db_conn.execute(query)

def db_update(db_conn, nom_tbl, hash, ips):
    query = "UPDATE {0} WHERE HASH={1} ips_bis" % (nom_tbl, hash)
    db_conn.execute(query)

def db_add(nom_tbl, nom, hash, ips):
    query = "INSERT INTO {0} ({1}, {2}, {3})" % (nom_tbl, nom, hash, pair)
    db_conn.execute(query)

def db_remove(db_conn, nom_tbl, hash):
    query = "DELETE FROM {0} WHERE HASH={1}" % (nom_tbl, hash)
    db_conn.execute(query)

def db_lookup():
    pass

if __name__  == '__main__':
    db_conn = sqlite3.connect(DB_NAME)
    db_curs = db_conn.cursor()


