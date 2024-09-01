import sqlite3

class DeviceDB():
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
            self.cur.execute('''CREATE TABLE IF NOT EXISTS device (id int, name text, serial text, app_count int, location text)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO device(id, name, serial) VALUES (?,?,?)"""
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
            self.cur.execute('SELECT id, name, serial, app_count, location FROM device')
            return self.cur.fetchall()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def delete_record(self):
        """ Delete the all record
        """
        try:
            self.cur.execute("DELETE FROM device")
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

class AccountDB():
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
            #['No', 'Status', 'Device Name', 'Account Name', 'UID', 'Page Name', 'Page ID', 'Password', '2FA', 'Token', 'Cookie', 'Package', 'Location', 'Store', 'Progress']
            self.cur.execute('''CREATE TABLE IF NOT EXISTS account (id INTEGER  primary key, status text, device int, acct_name text, acct_uid text, page_name text, page_id text, pass text, _2fa text, _token text, cookie text, app_pkg text, location text, store text, progress text)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO account (device, acct_name, acct_uid, pass, _2fa, store) VALUES (?,?,?,?,?,?)"""
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
            self.cur.execute('SELECT id, status, device, acct_name, acct_uid, page_name, page_id, pass, _2fa, _token, cookie, app_pkg, location, store, progress FROM account')
            return self.cur.fetchall()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def delete_record(self):
        """ Delete the all record
        """
        try:
            self.cur.execute("DELETE FROM account")
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

class PageDB():
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
            self.cur.execute('''CREATE TABLE IF NOT EXISTS page (id int primary key, acct_id int, name text)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO page VALUES (?,?,?)"""
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
            self.cur.execute('SELECT * FROM account')
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