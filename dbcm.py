import sqlite3
"""This is context manager module that manages database connections."""

class DBCM():
    """This class contains context manager"""
    def __init__(self, filename):
        self.filename = filename
        self.db = None
        self.cur = None

    def __enter__(self):
        """Opens the file and returns the file"""
        self.db = sqlite3.connect(self.filename)
        self.cur = self.db.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the file"""
        self.db.commit()
        self.db.close()
        self.cur.close