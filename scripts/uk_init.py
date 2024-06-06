from utils import create_connection, insert_user, insert_item
from create_tables import init_db

def main():
    init_db()
    
    database = "auction.db"
    conn = create_connection(database)

    # Create tables
    if conn is not None:

        # Insert unique users and items for Shard 1
        insert_user(conn, (5, 'User5', 'user5@example.com'))
        insert_user(conn, (6, 'User6', 'user6@example.com'))
        insert_item(conn, (5, 'Item5', None, 0.00))
        insert_item(conn, (6, 'Item6', None, 0.00))
        
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
