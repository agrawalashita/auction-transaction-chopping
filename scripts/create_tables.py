import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully Connected to SQLite database: {db_file}")
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """Create a table from the create_table_sql statement."""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully")
    except Error as e:
        print(e)

def main():
    database = "auction.db"

    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    );
    """

    sql_create_items_table = """
    CREATE TABLE IF NOT EXISTS Items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        high_bidder INTEGER,
        high_price DECIMAL(10, 2),
        FOREIGN KEY (high_bidder) REFERENCES Users(user_id)
    );
    """

    sql_create_bids_table = """
    CREATE TABLE IF NOT EXISTS Bids (
        bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
        bidder INTEGER,
        item INTEGER,
        bid_price DECIMAL(10, 2),
        FOREIGN KEY (bidder) REFERENCES Users(user_id),
        FOREIGN KEY (item) REFERENCES Items(item_id)
    );
    """

    # Create a database connection
    conn = create_connection(database)

    # Create tables
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_items_table)
        create_table(conn, sql_create_bids_table)
        
        # Close the connection
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
