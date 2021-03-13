#!/usr/local/bin/python3
import mysql.connector

from flask import g

config = {
    "host": "localhost",
    "user": "bluroom_takaaki",
    "password": "20210304",
    "database": "bluroom_takaaki",
    "use_unicode": True,
    "charset": "utf8"
}

def open_db():
    if "db" not in g:
        g.db = mysql.connector.connect(**config)
        g.db.row_factory = dict_factory
    return g.db

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def exec(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    db.commit()
    return c.lastrowid

def select(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    return c.fetchall()

def close_db(e=None):
    db = g.pop("db", None)
    
    if db is not None:
        db.close()

# 本番用
def init_app(app):
    app.teardown_appcontext(close_db)