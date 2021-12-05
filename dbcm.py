import sqlite3

class DBCM():
    def __init__(self, filename):
        self.filename = filename
        self.db = None
        self.cur = None

    def __enter__(self):
        self.db = sqlite3.connect(self.filename)
        self.cur = self.db.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.commit()
        self.db.close()
        self.cur.close