from utils import create_connection, insert_user, insert_item

def main():
    database = "auction.db"
    conn = create_connection(database)

    # Create tables
    if conn is not None:

        # Insert unique users and items for Shard 1
        insert_user(conn, (1, 'User1', 'user1@example.com'))
        insert_user(conn, (2, 'User2', 'user2@example.com'))
        
        insert_item(conn, (1, 'Item1', None, 0.00))
        insert_item(conn, (2, 'Item2', 'User3', 150.00))
        
        conn.close()
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
