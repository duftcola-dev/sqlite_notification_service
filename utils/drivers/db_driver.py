from os import curdir
import sqlite3
from main import Logs

class driver:

    def __init__(self,database:str,logs:Logs=None) -> None:
        if logs != None:
            self.logs=logs
        self.__con = None
        self.database = database
    

    def insert(self,query):
        cursor = self.__get_cursor()
        cursor.execute(query)
 
    def connect(self):
        try:
            self.__con = sqlite3.connect(self.database)
        except Exception as err:
            print(f"Cannot connect to database {err}")

    def close(self):
        self.__con.close()

    def __get_cursor(self):
        if self.__con != None:
            return self.__con.cursor()
        else: 
            raise Exception("Connection with database  : None")
    