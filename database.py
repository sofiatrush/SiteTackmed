import sqlite3
from flask import g
import os

class DatabaseManager:
    def __init__(self, database_path):
        self.database = database_path

    def get_db(self):
        if 'db' not in g:
            g.db = sqlite3.connect(self.database)
            g.db.row_factory = sqlite3.Row
        return g.db

    def init_db(self):
        db = self.get_db()

        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS results (
                username TEXT PRIMARY KEY,
                test1 INTEGER DEFAULT 0,
                test2 INTEGER DEFAULT 0,
                test3 INTEGER DEFAULT 0,
                test4 INTEGER DEFAULT 0,
                test5 INTEGER DEFAULT 0,
                test6 INTEGER DEFAULT 0,
                test7 INTEGER DEFAULT 0,
                test8 INTEGER DEFAULT 0,
                FOREIGN KEY (username) REFERENCES users(email)
            )
        ''')
        db.commit()

    def close_db(self, error):
        if hasattr(g, 'db'):
            g.db.close()
