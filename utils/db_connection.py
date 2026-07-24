import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None

    def __new__(cls, host="localhost", user="root", password="113355", database=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._instance.connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                cls._instance.cursor = cls._instance.connection.cursor(dictionary=True, buffered=True)
            except Error as e:
                print(f"Error connecting to MySQL: {e}")
                cls._instance = None
        return cls._instance

    def get_cursor(self):
        return self.cursor

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        DatabaseConnection._instance = None
