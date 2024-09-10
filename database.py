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
            self.cur.execute('''CREATE TABLE IF NOT EXISTS device (id int, name text, status text, serial text, app_count int, location text, enabled int)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO device(id, name, status, serial, enabled) VALUES (?,?,?,?,?)"""
        try:
            self.cur.execute(query, entities)
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)
        # self.conn.close()

    def update_device(self, devices):
        """ Update the table with given new values"""
        try:
            ld_list = []
            device_list = devices.list_ldplayer()
            for key, value in device_list.items():
                # print(key, value)
                ld_list.append(key)
                self.cur.execute("SELECT * FROM device WHERE id = ?", (key,))
                result = self.cur.fetchone()
                if result is None:
                    query = """INSERT INTO device(id, name, status, serial, enabled) VALUES (?,?,?,?,?)"""
                    try:
                        self.cur.execute(query, (key, value["name"], value["status"], value["serial"], 1))
                        self.conn.commit()
                    except sqlite3.IntegrityError as e:
                        print("Error name:", e.sqlite_errorname)
                else:                
                    self.cur.execute("UPDATE device SET name = ?, status = ?, serial = ?, enabled = ? WHERE id = ?", (value["name"], value["status"], value["serial"], 1, key))
                    self.conn.commit()
            # print(ld_list)
            self.cur.execute("SELECT * FROM device")
            rows = self.cur.fetchall()
            for row in rows:
                # print(row[0])
                if row[0] not in ld_list:
                    self.hide_device(row[0])

        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def hide_device(self, idx):
        self.cur.execute("UPDATE device SET enabled = ? WHERE id = ?", (0, idx))
        self.conn.commit()

    def select_all(self):
        """Selects all rows from the table to display
        """
        try:
            self.cur.execute('SELECT id, name, status, serial, app_count, location FROM device WHERE enabled=1')
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

class Setting():
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
            self.cur.execute('''CREATE TABLE IF NOT EXISTS setting (name text, value text)''')
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def insert_data(self, entities):
        """  Insert records into the table
        """
        query = """INSERT INTO setting(name, value) VALUES (?,?)"""
        try:
            name = entities[0]
            value = entities[1]
            exist_val = self.get_setting(name)
            if exist_val:
                self.cur.execute("UPDATE setting SET value = ? WHERE name = ?", (value, name,))
                self.conn.commit()
            else:
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
            self.cur.execute('SELECT * FROM setting')
            return self.cur.fetchall()
        except sqlite3.IntegrityError as e:
            print("Error name:", e.sqlite_errorname)

    def get_setting(self, param):
        """Selects a row from the table to display
        """
        try:
            self.cur.execute("SELECT value FROM setting WHERE name = ?", (param,))
            return self.cur.fetchone()
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