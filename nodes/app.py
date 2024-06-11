import websocket
import boto3
import threading
import json
from utils import send_message_to_connection
from transactions import transactions_us, transactions_in
from datetime import datetime
import sys

# Existing functions remain unchanged

transaction_start_times = {}
total_actual_latency = 0.0

def on_message(ws, message):
    try:
        data = json.loads(message)
        transaction_id = data['tid']
        if (data['current_hop'] == 1):
            end_time = datetime.now()

        # Process the data
        print("Received transaction result for: ", data, "\n")
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
    return [item['connectionId'] for item in connections if item['region'] == region and item['type'] == 'server']
    

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
    num_existing_records = int(sys.argv[2])

    if region == "us":
        transactions = transactions_us(num_existing_records)
    elif region == "in":
        transactions = transactions_in(num_existing_records)

    # Fetch all connection records from DynamoDB
    all_connections = fetch_connections()
    region_connections = filter_connections(all_connections, region)

    connection_id = region_connections[0]
    print(connection_id)

    for transaction_chain in transactions:
        print(transaction_chain)
        send_message_to_connection(connection_id, transaction_chain)

    websocket_thread.join()

if __name__ == '__main__':
    main()
