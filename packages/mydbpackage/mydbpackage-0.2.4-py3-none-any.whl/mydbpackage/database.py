# mydbpackage/database.py
import mysql.connector

column_names = []
class MyDB:
    def __init__(self, host, user, database):
        self.connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
        )
        self.cursor = self.connection.cursor()
    def create_table(self,table_name,column_name):
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY)"
        self.cursor.execute(create_table_query)
        for column in column_name:

            try:
                column_names.append(column)
                alter_query = f"ALTER TABLE {table_name} ADD COLUMN `{column}` TEXT"
                self.cursor.execute(alter_query)
            except mysql.connector.Error as err:
                if err.errno == 1060:  # Error number for duplicate column name
                    print(f"Column '{column}' already exists.")
                else:
                    print(f"Error adding column '{column}': {err}")

        self.connection.commit()

    def insert_log(self, list_value,table_name):
        # self.cursor.execute("INSERT INTO "+str(table_name) +" (url,status) VALUES (%s,%s)", (url,str(status)))
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'`{col}`' for col in column_names])}) VALUES ({', '.join(['%s'] * len(column_names))})"
        print(insert_query)


        for column in list_value:
            print(tuple(column))
            self.cursor.execute(insert_query, tuple(column))
        self.connection.commit()


    def get_users(self):
        self.cursor.execute("SELECT * FROM log")
        return self.cursor.fetchall()