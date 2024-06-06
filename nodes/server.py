import websocket
import sqlite3
import json
from utils import get_connections_from_dynamo, send_message_to_connection
import sys

DATABASE = 'auction.db'

server_connections = []
application_connections = []

def database_query(query):
    """Execute SQL on the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().lower().startswith('select'):
            return cursor.fetchall()  # Return query results for SELECT
        conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
        return "Query executed successfully."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def on_message(ws, message):
    transaction = json.loads(message)
    print(f"Received transaction: {transaction["tid"]}")

    global server_connections
    global application_connections
    
    if len(server_connections) == 0:
        server_connections = get_connections_from_dynamo(type="server")
        application_connections = get_connections_from_dynamo(type="application")
    
    current_hop = transaction["current_hop"]
    
    result = database_query(transaction["hops"][current_hop]["query"])

    # Reply to application after first hop
    application_connection_id = application_connections[transaction["hops"][current_hop]["origin_region"]]
    send_message_to_connection(connection_id=application_connection_id,message=result)
    
    # Send transaction to next hop if exists
    if len(transaction["hops"]) > current_hop + 1:
        next_hop_connection_id = server_connections[transaction["hops"][current_hop+1]["destination_region"]]

        transaction["current_hop"] = current_hop + 1
        
        send_message_to_connection(connection_id=next_hop_connection_id,message=transaction)

    print(f"Query result: {result}")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Connection opened")

if __name__ == "__main__":
    websocket.enableTrace(True)

    region = sys.argv[1]

    ws = websocket.WebSocketApp("wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=" + region + "&type=server",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
