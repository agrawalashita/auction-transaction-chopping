import websocket
import sqlite3
import json
# from utils import get_connections_from_dynamo, send_message_to_connection
from utils import get_connections_from_dynamo, send_message_to_connection
import sys
from scripts.india_init import india_init
from scripts.usa_init import usa_init
from scripts.uk_init import uk_init

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
        return {"message" : "Query executed successfully."}
    except Exception as e:
        return f"An error occurred while executing DB query: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def value_exists_in_dict(d, target_value):
    res = {}
    for key,value in d.items():
        if value == target_value:
            res[key] = value
    return res

def on_message(ws, message):
    transaction = json.loads(message)
    print(f"Received transaction: {transaction}")
    
    global ongoing_transactions
    global server_connections
    global application_connections

    existing_dependencies = value_exists_in_dict(ongoing_transactions, transaction["dependency"])

    print("Existing dependencies: ", existing_dependencies)

    if not existing_dependencies:
        transaction["wait_for_eids"] = existing_dependencies.keys()

    # wait for previous dependent transactions to complete
    while (True):
        print("enter while")
        flag = False
        for wait_for_eid in transaction["wait_for_eids"]:
            if wait_for_eid in ongoing_transactions.keys():
                flag = True
        
        if not flag:
            break
    
    if len(server_connections) == 0:
        server_connections = get_connections_from_dynamo(type="server")
        application_connections = get_connections_from_dynamo(type="application")
    
    print("going to run query")
    ongoing_transactions[transaction["eid"]] = transaction["tid"]

    current_hop = transaction["current_hop"]
    result = database_query(transaction["hops"][current_hop]["query"])

    print("Result of query:", result)

    # Reply to application after first hop
    application_connection_id = application_connections[transaction["hops"][current_hop]["origin_region"]]
    send_message_to_connection(connection_id=application_connection_id,message=result)

    # remove hop from ongoing transaction chops
    del ongoing_transactions[transaction["eid"]]
    
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
    region = sys.argv[1]

    if region == "us":
        usa_init()
    elif region == "in":
        india_init()
    elif region == "uk":
        uk_init()

    ws = websocket.WebSocketApp("wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=" + region + "&type=server",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
