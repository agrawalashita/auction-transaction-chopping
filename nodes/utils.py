import boto3
import json

WEBSOCKET_URL = 'https://hsslsryu8h.execute-api.us-east-1.amazonaws.com/dev'

def get_connections_from_dynamo(type):
    """Fetch all records from a DynamoDB table where 'type' column equals type
       and create a map of region to connectionId."""
    # Set up DynamoDB connection
    # Create a session with a specific region
    session = boto3.Session(region_name='us-east-1')

    # Now get the DynamoDB resource using this session
    dynamodb = session.resource('dynamodb')

    table = dynamodb.Table('CS223P_Connections')  # Replace with your table name

    region_to_connection_id_map = {}  # Dictionary to hold the mapping

    try:
        # Perform a scan operation with a filter expression to retrieve only items where 'type' equals 'server'
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('type').eq(type)
        )
        # Iterate over items to populate the map
        for item in response['Items']:
            # Assuming 'region' and 'connectionId' are the keys in the DynamoDB items
            region = item.get('region')
            connection_id = item.get('connectionId')
            if region and connection_id:
                region_to_connection_id_map[region] = connection_id
        return region_to_connection_id_map
    except Exception as e:
        print(f"Failed to fetch data from DynamoDB: {str(e)}")
        return {}

def send_message_to_connection(connection_id, message):
    """Send a message to a WebSocket connection via AWS API Gateway."""
    client = boto3.client('apigatewaymanagementapi', endpoint_url=WEBSOCKET_URL, region_name="us-east-1")
    try:
        response = client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(message.encode('utf-8'))
        )
        print(f"Got response: {response}")
    except client.exceptions.GoneException:
        print(f"The connection {connection_id} is no longer available.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")