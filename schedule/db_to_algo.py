import sqlite3
import csv

class db_helper:
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()

    def read_db(self, sqlite):
        pass
    
    def print_all_columns(self,table_name):
        c = self.cursor
        #if "\" in 
        c.execute(f'SELECT * FROM {table_name}')
        print(list(map(lambda x: x[0], c.description)))

    def get_columns(self,list_of_columns,table_name):
        c = self.cursor
        a = ""
        for i in list_of_columns:
            a += i + ","
            print(i)
        a = a[0:len(a)-1]
        c.execute(f"SELECT {a} FROM {table_name}") 
        return c.fetchall()

    # Takes input from algorithm and puts it back into the classtable
    def update_db(self, data):
        for i in data:
            _id = i[0]
            day = i[3]
            start = i[4]
            end = i[5]
            self.cursor.execute(f"UPDATE users_class SET day='{day}', start='{start}', end='{end}' WHERE id = {_id}")
            print("wrote")
        self.conn.commit()


    def make_input(id, data):
        c = self.cursor
        c.execute()

    def get_input():
        pass

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)
        return None