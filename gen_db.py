#!/usr/bin/env python3.5
import sqlite3, cakebot_config
conn = sqlite3.connect(cakebot_config.DB_PATH)
c = conn.cursor()

print("Dropping tables...")
try:
    c.execute('DROP TABLE log_channel')
    c.execute('DROP TABLE music_prefix')
    c.execute('DROP TABLE permissions')
    c.execute('DROP TABLE songs')
except sqlite3.OperationalError:
    pass

print("Creating empty tables...")
c.execute('''CREATE TABLE music_prefix(
    id          INTEGER NOT NULL PRIMARY KEY,
    server_id   TEXT,
    prefix      TEXT)''')
c.execute('''CREATE TABLE permissions(
    id          INTEGER NOT NULL PRIMARY KEY,
    user_id     TEXT NOT NULL,
    server_id   TEXT NOT NULL,
    permissions TEXT)''')
c.execute('''CREATE TABLE songs(
    id          INTEGER NOT NULL PRIMARY KEY,
    name        TEXT NOT NULL,
    artist      TEXT,
    album       TEXT,
    link        TEXT NOT NULL,
    alias       TEXT)''')
c.execute('''CREATE TABLE log_channel(
    id          INTEGER NOT NULL PRIMARY KEY,
    server_id   TEXT NOT NULL,
    channel_id  TEXT NOT NULL)''')
conn.commit()
conn.close()