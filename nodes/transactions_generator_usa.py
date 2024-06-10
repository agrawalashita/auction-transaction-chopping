import random

NUM_TYPES = 6

def generate_t1(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        bid_price = random.randint(5, 50) * 10  # Generate a random bid price between 50 and 500
        transaction = {
            "tid": "t1",
            "eid": f"execution_{i}",
            "dependency": "t1",
            "current_hop": 0,
            "hops": [
                {
                    # Insert bid with incrementing bid_id and random bid price
                    "query": f"INSERT INTO Bids (bid_id, bidder, item, bid_price) VALUES ({i}, 1, 3, {bid_price});",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    # Update item with the same random bid price
                    "query": f"UPDATE Items SET high_price = {bid_price}, high_bidder = 1 WHERE item_id = 3 AND {bid_price} > high_price;",
                    "origin_region": "us",
                    "destination_region": "in"
                }
            ]
        }
        transactions.append(transaction)  # Add the transaction to the list

    return transactions


def generate_t2(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        description = f'Item{i}'  # Increment description accordingly

        transaction = {
            "tid": "t2",
            "eid": f"execution_{i}",  # Each transaction gets a unique execution ID
            "current_hop": 0,
            "hops": [
                {
                    "query": f"INSERT INTO Items (item_id, description, high_bidder, high_price) VALUES ({i}, '{description}', NULL, 0.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        }
        transactions.append(transaction)

    return transactions


def generate_t3(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        transaction = {
            "tid": "t3",
            "eid": f"execution_{i}",
            "current_hop": 0,
            "hops": [
                {
                    "query": "SELECT * FROM Items WHERE item_id = 1;",  # Query remains the same for each transaction
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        }
        transactions.append(transaction)

    return transactions

def generate_t4(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        transaction = {
            "tid": "t4",
            "eid": f"execution_{i}",  # Unique execution ID for each transaction
            "current_hop": 0,
            "hops": [
                {
                    # Insert record into ItemsSold for the US region
                    "query": f"INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES ({i}, 10001, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    # Replicate the winning bid to the India region
                    "query": f"INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES ({i}, 10001, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "in"
                },
                {
                    # Replicate the winning bid to the UK region
                    "query": f"INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES ({i}, 10001, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "uk"
                }
            ]
        }
        transactions.append(transaction)
        
    return transactions

def generate_t5(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        user_id = i  # Increment user_id starting from 1
        username = f'User{user_id}'
        email = f'user{user_id}@example.com'
        
        transaction = {
            "tid": "t5",
            "eid": f"execution_{i}",  # Unique execution ID for each transaction
            "current_hop": 0,
            "hops": [
                {
                    "hop": 1,
                    "query": f"INSERT INTO Users (user_id, username, email) VALUES ({user_id}, '{username}', '{email}');",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        }
        transactions.append(transaction)

    return transactions

def generate_t6(start, end):
    transactions = []  # Initialize an empty list to hold all transactions

    for i in range(start, end):
        transaction = {
            "tid": "t6",
            "eid": "execution_6",
            "current_hop": 0,
            "hops": [
                {
                    "query": "UPDATE Users SET email = 'user1new@example.com' WHERE user_id = 1;",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        }
        transactions.append(transaction)

    return transactions