import mysql.connector
from mysql.connector import pooling

class DatabaseConnectionPool:
    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseConnectionPool.__instance is None:
            DatabaseConnectionPool()
        return DatabaseConnectionPool.__instance

    def __init__(self):
        if DatabaseConnectionPool.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="my_pool",
                    pool_size=10,
                    host='localhost',
                    user='root',
                    password='firman25',
                    database='tugas_akhir'
                )
                DatabaseConnectionPool.__instance = self
                print("Connection pool created")
            except Exception as e:
                print("Error creating connection pool:", str(e))
