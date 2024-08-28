import sqlite3


# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS device(id int, name text, port text, status text)''')

# Insert a row of data
cursor.execute("INSERT INTO device VALUES ('3','LDPlayer 3','emulator-5558','running')")

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()