import sqlite3
from flask import g, current_app
DATABASE = 'db.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if one else rv) if rv else (None if one else [])

def add_user(username, hashed_password):
    db = get_db()
    db.execute('INSERT INTO accounts (username, password) VALUES (?, ?)', (username, hashed_password))
    db.commit()

def init_db():
    db = get_db()
    # Directly executing CREATE TABLE statements within Python
    db.executescript('''
    CREATE TABLE IF NOT EXISTS accounts (
        rowid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        salt TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS profiles (
        userid INTEGER PRIMARY KEY,
        fname TEXT,
        lname TEXT,
        avatar TEXT,
        files TEXT,
        FOREIGN KEY(userid) REFERENCES accounts(rowid)
    );
    ''')


