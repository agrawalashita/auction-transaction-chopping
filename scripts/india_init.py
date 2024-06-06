from utils import create_connection, insert_user, insert_item, insert_bid
from create_tables import init_db

def main():
    init_db()
    
    database = "auction.db"
    conn = create_connection(database)

    # Create tables
    if conn is not None:

        # Insert unique users and items for Shard 1
        insert_user(conn, (3, 'User3', 'user3@example.com'))
        insert_user(conn, (4, 'User4', 'user4@example.com'))

        insert_item(conn, (3, 'Item3', None, 0.00))
        insert_item(conn, (4, 'Item4', None, 0.00))
        
        insert_bid(conn, (3, 'User3', 'Item2', 150.00))
        
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
