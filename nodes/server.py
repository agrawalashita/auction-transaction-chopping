import websocket
import sqlite3
import json
# from utils import get_connections_from_dynamo, send_message_to_connection
from utils import get_connections_from_dynamo, send_message_to_connection
import sys
from scripts.insert_records import initialize_region

import time

DATABASE = 'auction.db'

server_connections = []
application_connections = []
ongoing_transactions = {}

def database_query(query):
    """Execute SQL on the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().lower().startswith('select'):
            return cursor.fetchall()  # Return query results for SELECT
        conn.commit()  # Commit changes for INSERT, UPDATE, DELETE
        return "Query executed successfully"
    except Exception as e:
        return f"An error occurred while executing DB query: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def value_exists_in_dict(d, transaction):
    if "dependency" not in transaction:
        return {}
    res = {}
    target_value = transaction["dependency"]
    for key,value in d.items():
        if value == target_value:
            res[key] = value
    return res

def on_message(ws, message):
    global total_perceived_latency

    transaction = json.loads(message)
    print(f"Received transaction: {transaction}\n")
    
    global ongoing_transactions
    global server_connections
    global application_connections

    existing_dependencies = value_exists_in_dict(ongoing_transactions, transaction)

    if len(existing_dependencies.keys()) > 0:
        transaction["wait_for_eids"] = list(existing_dependencies.keys())

    # wait till dependent transaction completes its hops on same server
    if "wait_for_eids" in transaction:
        while True:
            flag = False
            for wait_for_eid in transaction["wait_for_eids"]:
                if wait_for_eid in ongoing_transactions.keys():
                    flag = True
            
            if not flag:
                break
    
    if len(server_connections) < 2:
        server_connections = get_connections_from_dynamo(type="server")

    if len(application_connections) < 2:
        application_connections = get_connections_from_dynamo(type="application")
    
    ongoing_transactions[transaction["eid"]] = transaction["tid"]

    # print("Ongoing transactions: ", ongoing_transactions)

    current_hop = transaction["current_hop"]
    result = database_query(transaction["hops"][current_hop]["query"])

    # Reply to application after first hop
    print(f"Hop {current_hop+1} of Transaction", transaction["tid"], ":", transaction["hops"][current_hop])

    if (current_hop == 0 or len(transaction["hops"]) == current_hop + 1):
        application_connection_id = application_connections[transaction["hops"][current_hop]["origin_region"]]
        send_message_to_connection(connection_id=application_connection_id,message=transaction)
    
    # remove hop from ongoing transaction chops
    del ongoing_transactions[transaction["eid"]]
    
    # Send transaction to next hop if exists
    if len(transaction["hops"]) > current_hop + 1:
        next_hop_connection_id = server_connections[transaction["hops"][current_hop+1]["destination_region"]]

        transaction["current_hop"] = current_hop + 1
        
        send_message_to_connection(connection_id=next_hop_connection_id,message=transaction)

    print(f"Query result: {result}\n\n")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Web Socket Connection opened\n")

if __name__ == "__main__":
    region = sys.argv[1]
    num_records = int(sys.argv[2])

    initialize_region(region, num_records)

    ws = websocket.WebSocketApp("wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=" + region + "&type=server",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
