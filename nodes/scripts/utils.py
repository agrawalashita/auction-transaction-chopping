import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by the db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Successfully connected to SQLite database: {db_file}")
    except Error as e:
        print(e)
    return conn

def insert_user(conn, user):
    """Insert a new user into the Users table."""
    sql = ''' INSERT INTO Users(user_id, username, email)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid

def insert_item(conn, item):
    """Insert a new item into the Items table."""
    sql = ''' INSERT INTO Items(item_id, description, high_bidder, high_price)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid

def insert_bid(conn, item):
    """Insert a new item into the Items table."""
    sql = ''' INSERT INTO Bids(bid_id, bidder, item, bid_price)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid