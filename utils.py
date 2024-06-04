import boto3

def get_connections():
    """Fetch all records from a DynamoDB table where 'type' column equals 'server'
       and create a map of region to connectionId."""
    # Set up DynamoDB connection
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CS223P_Connections')  # Replace with your table name

    region_to_connection_id_map = {}  # Dictionary to hold the mapping

    try:
        # Perform a scan operation with a filter expression to retrieve only items where 'type' equals 'server'
        response = table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('type').eq('server')
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