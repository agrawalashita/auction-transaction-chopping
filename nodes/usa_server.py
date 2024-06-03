import websocket
import sqlite3

DATABASE = 'auction.db'

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
    print(f"Received message: {message}")
    response = database_query(message["data"])
    # post websocket to usa_app
    # update item in india bid
    print(f"Query result: {response}")
    return "Executed query successfully"

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Connection opened")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev/?region=us",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
