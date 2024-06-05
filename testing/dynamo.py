import boto3

session = boto3.Session(region_name='us-east-1')
dynamodb = session.resource('dynamodb')

table = dynamodb.Table("CS223P_Connections")
response = table.scan()  # Fetches all records, consider using pagination for large datasets

print(response['Items'])