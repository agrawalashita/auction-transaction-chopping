import sqlite3

def drop_all_tables(db_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Retrieve a list of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Generate and execute DROP TABLE commands for each table
    cursor.executescript(';'.join([f"DROP TABLE IF EXISTS {table[0]}" for table in tables]))
    
    print(f"All tables have been dropped from the database '{db_name}'.")
    
    # Commit changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

# Usage
db_name = 'auction.db'
drop_all_tables(db_name)
