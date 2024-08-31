import sqlite3

class DB():
    def __init__(self):
        try:
            self.conn = sqlite3.connect('database.db')
            self.cur = self.conn.cursor() 
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def create_table(self):
        """ Create the table with given columns
        """
        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS device (id int, name text, port text, status text)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO device VALUES (?,?,?,?)"""
        try:
            self.cur.execute(query, entities)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)
        # self.conn.close()

    def update_data(self, entities):
        """ Update the table with given new values"""
        try:
            self.cur.execute("UPDATE device SET name = ?, status =? WHERE id = ?", entities)
            self.conn.commit()
            print("The record updated successfully")
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def select_all(self):
        """Selects all rows from the table to display
        """
        try:
            self.cur.execute('SELECT * FROM device')
            return self.cur.fetchall()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def delate_record(self):
        """ Delete the all record
        """
        try:
            self.cur.execute("DELETE FROM device")
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)
