# scripts/region_init.py
import random
import sys
from scripts.scripts_utils import create_connection, insert_user, insert_item, insert_bid
from scripts.create_tables import init_db

# Define global ID ranges for each region
USA_RANGE = (1, 10000)
INDIA_RANGE = (10001, 20000)
UK_RANGE = (20001, 30000)

def select_high_bidder(current_region):
    """Select a random high bidder ID from the other two regions."""
    if current_region == 'usa':
        return random.choice(list(range(*INDIA_RANGE)) + list(range(*UK_RANGE)))
    elif current_region == 'india':
        return random.choice(list(range(*USA_RANGE)) + list(range(*UK_RANGE)))
    elif current_region == 'uk':
        return random.choice(list(range(*USA_RANGE)) + list(range(*INDIA_RANGE)))

def init_region_data(region_name, start_id, end_id, num_records):
    database = f"auction.db"
    init_db(database)  # Initialize database, which includes creating tables and removing old db file
    conn = create_connection(database)

    print(f"Inserting {num_records} per table")

    if conn is not None:
        for user_id in range(start_id, start_id + num_records):
            username = f'User{user_id}'
            email = f'user{user_id}@example.com'
            insert_user(conn, (user_id, username, email))

            item_id = user_id
            description = f'Item{user_id}'
            high_bidder = select_high_bidder(region_name)  # Ensure every item has a high bidder
            high_price = round(random.uniform(50, 500) / 10) * 10  # Ensure high_price is a multiple of 10
            insert_item(conn, (item_id, description, high_bidder, high_price))

            bid_id = user_id
            bid_price = high_price
            insert_bid(conn, (bid_id, high_bidder, item_id, bid_price))

        conn.close()
    else:
        print("Error! cannot create the database connection.")

def initialize_region(region, num_records):
    if region == 'us':
        init_region_data('us', *USA_RANGE, num_records)
    elif region == 'in':
        init_region_data('in', *INDIA_RANGE, num_records)
    elif region == 'uk':
        init_region_data('uk', *UK_RANGE, num_records)
