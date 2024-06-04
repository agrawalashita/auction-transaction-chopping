import boto3

def get_connections():
    """Fetch all records from a DynamoDB table without handling pagination."""
    # Set up DynamoDB connection
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CS223P_Connections')  # Replace with your table name

    try:
        # Perform a scan operation to retrieve all items from the table
        response = table.scan()
        # This will only fetch data up to 1 MB or the table's full data if less than 1 MB
        data = response['Items']
        return data
    except Exception as e:
        print(f"Failed to fetch data from DynamoDB: {str(e)}")
        return []