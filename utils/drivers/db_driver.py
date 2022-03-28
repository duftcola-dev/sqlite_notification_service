import sqlite3
from notifications.Logs import Logs

class driver:

    def __init__(self,database:str,logs:Logs=None) -> None:
        try:
            if logs != None:
                self.logs=logs
            self.cursor = None
            self.con = sqlite3.connect(database)
            self.cursor = self.con.cursor()
            
        except Exception as err:
            print(f"Cannot connect to database {err}")


    def close(self):
        self.con.close()
