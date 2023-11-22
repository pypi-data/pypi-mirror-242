# mydbpackage/database.py
import mysql.connector

class MyDB:
    def __init__(self, host, user, database):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
        )
        self.cursor = self.connection.cursor()

    def create_table(self,table_name):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS '''+str(table_name) +'''
                              (id INT AUTO_INCREMENT PRIMARY KEY, url VARCHAR(255) NOT NULL, status VARCHAR(255) NOT NULL)''')
        self.connection.commit()

    def insert_log(self, url,status):
        self.cursor.execute("INSERT INTO log (url,status) VALUES (%s,%s)", (url,str(status)))
        self.connection.commit()

    def get_users(self):
        self.cursor.execute("SELECT * FROM log")
        return self.cursor.fetchall()