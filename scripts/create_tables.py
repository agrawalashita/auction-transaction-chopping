import sqlite3

# Connect to SQLite database or create it if it doesn't exist
conn = sqlite3.connect('auction.db')

# SQL script as a multi-line string
sql_script = """
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    seller INTEGER,
    high_bidder INTEGER,
    high_price DECIMAL(10, 2),
    status TEXT DEFAULT 'available',
    FOREIGN KEY (seller) REFERENCES Users(user_id),
    FOREIGN KEY (high_bidder) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Bids (
    bid_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bidder INTEGER,
    item INTEGER,
    bid_price DECIMAL(10, 2),
    FOREIGN KEY (bidder) REFERENCES Users(user_id),
    FOREIGN KEY (item) REFERENCES Items(item_id)
);

CREATE TABLE IF NOT EXISTS EmailNotifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS AuditLogs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action_description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE IF NOT EXISTS Notifications (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    notification_text TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
"""

# Execute the SQL script
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()

# Close the connection
conn.close()
