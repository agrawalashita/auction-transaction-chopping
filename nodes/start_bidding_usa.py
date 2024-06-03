import boto3

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

def main():
    # Configuration
    dynamodb_table = 'CS223P_Connections'
    api_gateway_management_api = 'https://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev'

    # Transactions to be sent
    transactions = [
        "BEGIN; INSERT INTO Bids (bidder, item, bid_price) VALUES (1, 1, 200.00); UPDATE Items SET high_price = 200.00, high_bidder = 1 WHERE item_id = 1 AND 200.00 > high_price; COMMIT;",
        "INSERT INTO Items (description, high_bidder, high_price) VALUES ('Antique vase', NULL, 0.00);",
        "SELECT * FROM Items;",
        "INSERT INTO Users (username, email) VALUES ('john_doe', 'john@example.com');",
        "UPDATE Users SET email = 'new_email@example.com' WHERE user_id = 1;",
        "SELECT * FROM Users;"
    ]

    # Fetch all connection records from DynamoDB
    all_connections = fetch_connections(dynamodb_table)

    # Filter for USA connections
    usa_connections = filter_usa_connections(all_connections)

    # Send each transaction to all USA connection IDs
    for connection_id in usa_connections:
        for transaction in transactions:
            send_message_to_connection(api_gateway_management_api, connection_id, transaction)

if __name__ == '__main__':
    main()
