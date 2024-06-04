import boto3
import websocket

running_transactions = []

def fetch_connections(dynamodb_table):
    """Fetch all connection records from DynamoDB."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table)
    response = table.scan()  # Fetches all records, consider using pagination for large datasets
    return response['Items']

def filter_usa_connections(connections):
    """Filter connections for those in the 'USA' region."""
    return [item['connectionId'] for item in connections if item['region'] == 'us']

def send_message_to_connection(api_gateway_management_api, connection_id, message):
    """Send a message to a WebSocket connection via AWS API Gateway."""
    client = boto3.client('apigatewaymanagementapi', endpoint_url=api_gateway_management_api)
    try:
        response = client.post_to_connection(
            ConnectionId=connection_id,
            Data=message.encode('utf-8')
        )
        print(f"Got response: {response}")
    except client.exceptions.GoneException:
        print(f"The connection {connection_id} is no longer available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def open_websocket(url):
    """Open a WebSocket and send a message."""
    ws = websocket.create_connection(url)
    return ws

def main():
    # Configuration
    dynamodb_table = 'CS223P_Connections'
    api_gateway_management_api = 'https://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev'
    websocket_url = 'ws://example.com/websocket'

    ws = open_websocket(websocket_url)
    print("WebSocket connection opened")

    # Transactions to be sent

    transactions = [
        {
            "t1": [
                {
                    "query": "INSERT INTO Bids (bidder, item, bid_price) VALUES (1, 1, 200.00);",
                    "origin_region": "us",
                    "destination_region": "us"
                },
                {
                    "query": "UPDATE Items SET high_price = 200.00, high_bidder = 1 WHERE item_id = 1 AND 200.00 > high_price;",
                    "origin_region": "in",
                    "destination_region": "in"
                }
            ],
            "t2": {
                "query": "INSERT INTO Items (description, high_bidder, high_price) VALUES ('Antique vase', NULL, 0.00);",
                "origin_region": "us",
                "destination_region": "us"
            },
            "t3": {
                "query": "SELECT * FROM Items;",
                "origin_region": "us",
                "destination_region": "us"
            },
            "t4": {
                "query": "INSERT INTO Users (username, email) VALUES ('john_doe', 'john@example.com');",
                "origin_region": "us",
                "destination_region": "us"
            },
            "t5": {
                "query": "UPDATE Users SET email = 'new_email@example.com' WHERE user_id = 1;",
                "origin_region": "us",
                "destination_region": "us"
            },
            "t6": {
                "query": "SELECT * FROM Users;",
                "origin_region": "us",
                "destination_region": "us"
            }
        }
    ]

    # Fetch all connection records from DynamoDB
    all_connections = fetch_connections(dynamodb_table)

    # Filter for USA connections
    usa_connections = filter_usa_connections(all_connections)

    # Send each transaction to all USA connection IDs
    for connection_id in usa_connections:
        # Assuming transactions is structured as a list of dictionaries as previously corrected
        for transaction_group in transactions:  # There is only one element in this example
            for transaction_key, transaction_details in transaction_group.items():
                # Send the message for each transaction. transaction_details contains the transaction data
                send_message_to_connection(api_gateway_management_api, connection_id, transaction_details)
                running_transactions.append(transaction_key)

        # for transaction in transactions:
        #     send_message_to_connection(api_gateway_management_api, connection_id, transaction)

    ws.close()
    print("WebSocket connection closed")
    

if __name__ == '__main__':
    main()
