import websocket
import boto3
import threading
import json

running_transactions = []

# Existing functions remain unchanged

def on_message(ws, message):
    print(f"Received message: {message}")

    try:
        data = json.loads(message)
        # Process the data
        print("Processing received data...", data)
    except json.JSONDecodeError:
        print("Error decoding the JSON message")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### WebSocket Closed ###")

def on_open(ws):
    print("WebSocket connection opened")

def start_websocket(url):
    ws = websocket.WebSocketApp(url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

def fetch_connections(dynamodb_table):
    """Fetch all connection records from DynamoDB."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table)
    response = table.scan()  # Fetches all records, consider using pagination for large datasets
    return response['Items']

def filter_usa_connections(connections):
    """Filter connections for those in the 'USA' region."""
    return [item['connectionId'] for item in connections if item['region'] == 'us']
    

def main():
    # Configuration for WebSocket
    websocket_url = "wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=us&type=application"

    # Start WebSocket in a separate thread
    websocket_thread = threading.Thread(target=start_websocket, args=(websocket_url,))
    websocket_thread.start()

    # Existing main functionality continues here...
    # Fetch and send messages as before
    dynamodb_table = 'CS223P_Connections'
    api_gateway_management_api = 'https://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev'
    all_connections = fetch_connections(dynamodb_table)
    usa_connections = filter_usa_connections(all_connections)

    # Sample transactions from your script
    transactions = [
        {
            "tid": "t1",
            "current_hop": 0,
            "hops": [
                {
                    "query": "INSERT INTO Items (description, high_bidder, high_price) VALUES ('Antique vase', NULL, 0.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            "tid": "t2",
            "current_hop": 0,
            "hops": [
                {
                    "query": "SELECT * FROM Items;",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            "tid": "t3",
            "current_hop": 0,
            "hops": [
                {
                    "hop": 1,
                    "query": "INSERT INTO Users (username, email) VALUES ('john_doe', 'john@example.com');",
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
                    "query": "UPDATE Users SET email = 'new_email@example.com' WHERE user_id = 1;",
                    "origin_region": "us",
                    "destination_region": "us"
                }
            ]
        },
        {
            "tid": "t5",
            "current_hop": 0,
            "hops": [
                {
                    "query": "SELECT * FROM Users;",
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
                    "query": "INSERT INTO Bids (bidder, item, bid_price) VALUES (1, 1, 200.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    "query": "UPDATE Items SET high_price = 200.00, high_bidder = 1 WHERE item_id = 1 AND 200.00 > high_price;",
                    "origin_region": "us",
                    "destination_region": "in"
                }
            ]
        }
    ]



    # Fetch all connection records from DynamoDB
    all_connections = fetch_connections(dynamodb_table)

    # Filter for USA connections
    usa_connections = filter_usa_connections(all_connections)
    connection_id = usa_connections[0]

    for transaction_chain in transactions:
        send_message_to_connection(api_gateway_management_api, connection_id, transaction_chain)
        running_transactions.append(transaction_chain["tid"])

    websocket_thread.join()

if __name__ == '__main__':
    main()
