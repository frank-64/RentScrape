import sqlite3
import os

class SQLiteDB:
    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        self.conn.commit()
        self.conn.close()

    def execute_query(self, query, params=()):
        self.cursor.execute(query, params)

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def destroy(self):
        if self.db_name != ":memory:" and os.path.exists(self.db_name):
            os.remove(self.db_name)