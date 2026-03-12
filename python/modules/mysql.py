import pymysql

class MySQL:
    def __init__(self, host="127.0.0.1", user='root', password='', database='livraria'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database,
            cursorclass = pymysql.cursors.DictCursor
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, parameters=None):
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(query, parameters)
            except Exception as e:
                self.connection.rollback()
                print(f"Error on execute query: {e}")
                raise e
            else:
                if cursor.description:
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return cursor.lastrowid

 