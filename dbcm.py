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
            self.database = None
            self.cur = None
        except Exception as error:
            logging.error("DBCM:init", error)


    def __enter__(self):
        """Opens the file and returns the file"""
        try:
            self.database = sqlite3.connect(self.filename)
            self.cur = self.database.cursor()
            return self.cur
        except Exception as error:
            logging.error("DBCM:enter", error)

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the file"""
        try:
            self.database.commit()
            self.database.close()
            self.cur.close
        except Exception as error:
            logging.error("DBCM:exit", error)
