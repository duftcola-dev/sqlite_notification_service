import sqlite3


class driver:

    def __init__(self,database:str,logs:object=None) -> None:
        if logs != None:
            self.logs=logs
        self.__con = None
        self.database = database
    

    def insert(self,query):
        cursor = self.__get_cursor()
        result = cursor.execute(query[0],query[1])
        self.save()
        return result
 
    def save(self):
        self.__con.commit()

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
    