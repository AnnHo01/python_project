"""This is context manager module that manages database connections."""
import logging
import sqlite3

logging.basicConfig(filename='status.log', format='%(asctime)s %(message)s', level=logging.NOTSET)
logging.info("Start logging")



class DBCM():
    """This class contains context manager"""
    def __init__(self, filename):
        try:
            self.filename = filename
            self.db = None
            self.cur = None
        except Exception as e:
            logging.error("DBCM:init", e)


    def __enter__(self):
        """Opens the file and returns the file"""
        try:
            self.db = sqlite3.connect(self.filename)
            self.cur = self.db.cursor()
            return self.cur
        except Exception as e:
            logging.error("DBCM:enter", e)

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the file"""
        try:
            self.db.commit()
            self.db.close()
            self.cur.close
        except Exception as e:
            logging.error("DBCM:exit", e)