transactions_us = [
        {
            ## Place bid for item in India
            "tid": "t1",
            "current_hop": 0,
            "hops": [
                {
                    # User1 of USA bids for Item3 in India for $200
                    "query": "INSERT INTO Bids (bid_id, bidder, item, bid_price) VALUES (1, 1, 3, 200.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    "query": "UPDATE Items SET high_price = 200.00, high_bidder = 1 WHERE item_id = 3 AND 200.00 > high_price;",
                    "origin_region": "us",
                    "destination_region": "in"
                }
            ]
        },
        {
            ## Place item for auction in USA
            "tid": "t2",
            "current_hop": 0,
            "hops": [
                {
                    "query": "INSERT INTO Items (item_id, description, high_bidder, high_price) VALUES (7, 'Item7', NULL, 0.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            ## Check status of bid on an item in US
            "tid": "t3",
            "current_hop": 0,
            "hops": [
                {
                    "query": "SELECT * FROM Items WHERE item_id = 1;",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            "tid": "t4",
            "current_hop": 0,
            "hops": [
                {
                    ## User3 from India won bid for Item2 in USA and replicated to all servers
                    "query": "INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES (2, 3, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    ## User3 from India won bid for Item2 in USA and replicated to all servers
                    "query": "INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES (2, 3, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "in"
                },
                {
                    ## User3 from India won bid for Item2 in USA and replicated to all servers
                    "query": "INSERT INTO ItemsSold (item_id, winning_bidder, sold_price, sold_date) VALUES (2, 3, 150, '2024-01-01 10:00:00')",
                    "origin_region": "us",
                    "destination_region": "uk"
                }
            ]
        },
        {
            "tid": "t5",
            "current_hop": 0,
            "hops": [
                {
                    "hop": 1,
                    "query": "INSERT INTO Users (user_id, username, email) VALUES (7, 'User7', 'user7@example.com');",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            "tid": "t6",
            "current_hop": 0,
            "hops": [
                {
                    "query": "UPDATE Users SET email = 'user1new@example.com' WHERE user_id = 1;",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        }
    ]

transactions_in = []
transactions_uk = []