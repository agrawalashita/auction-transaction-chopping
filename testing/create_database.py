import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect('auction_db.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table as per requirement
sql ='''CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)'''

cursor.execute(sql)

# Insert data into table
cursor.execute("INSERT INTO Users (username, email) VALUES ('newUser', 'user@example.com')")

# Commit your changes in the database
conn.commit()

# Retrieving data
cursor.execute("SELECT * from Users")

# Fetch and display result
for row in cursor.fetchall():
    print(row)

# Closing the connection
conn.close()
