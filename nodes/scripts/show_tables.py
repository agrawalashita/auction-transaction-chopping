import sqlite3

def create_connection(db_file):
    """Create a database connection to a SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite database: {db_file}")
    except sqlite3.Error as e:
        print(e)
    return conn

def select_all(conn, table_name):
    """Query all rows in the given table and print the results."""
    cur = conn.cursor()
    query = f"SELECT * FROM {table_name};"
    try:
        cur.execute(query)
        rows = cur.fetchall()
        # Print the results
        print(f"Data from {table_name}:")
        for row in rows:
            print(row)
    except sqlite3.Error as e:
        print(f"Failed to retrieve data from {table_name}: {e}")

def main():
    database = "auction.db"  # Adjust the path to your SQLite database file

    # Create a database connection
    conn = create_connection(database)
    
    if conn is not None:
        # Query and display all records from Bids
        select_all(conn, "Bids")
        
        # Query and display all records from Items
        select_all(conn, "Items")
        
        # Close the connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
