import websocket
import boto3
import threading
import json
from nodes.utils import send_message_to_connection
from transactions import transactions_us, transactions_in, transactions_uk
import sys

running_transactions = []

# Existing functions remain unchanged

def on_message(ws, message):
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

def fetch_connections():
    """Fetch all connection records from DynamoDB."""
    session = boto3.Session(region_name='us-east-1')
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table("CS223P_Connections")
    response = table.scan()  # Fetches all records, consider using pagination for large datasets
    return response['Items']

def filter_connections(connections, region):
    """Filter connections for those in the 'USA' region."""
    return [item['connectionId'] for item in connections if item['region'] == region]
    

def main():
    # Configuration for WebSocket
    region = sys.argv[1]
    websocket_url = "wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=" + region + "&type=application"

    # Start WebSocket in a separate thread
    websocket_thread = threading.Thread(target=start_websocket, args=(websocket_url,))
    websocket_thread.start()

    # Sample transactions from your script
    transactions = []

    region = sys.argv[1]
    if region == "us":
        transactions = transactions_us
    elif region == "in":
        transactions = transactions_in
    elif region == "uk":
        transactions = transactions_uk

    # Fetch all connection records from DynamoDB
    all_connections = fetch_connections()
    usa_connections = filter_connections(all_connections, region)

    connection_id = usa_connections[0]
    print(connection_id)

    for transaction_chain in transactions:
        send_message_to_connection(connection_id, transaction_chain)
        running_transactions.append(transaction_chain["tid"])

    websocket_thread.join()

if __name__ == '__main__':
    main()
