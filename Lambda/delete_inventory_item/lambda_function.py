import boto3
import json
import decimal  # Add this import to fix the error

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Extract the 'id' from the path parameters (only 'id' now, no 'location_id')
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # Query to fetch item based on just the PK (item_id)
    try:
        response = dynamo_client.query(
            TableName=table_name,
            KeyConditionExpression="item_id = :pk",  # PK is item_id in this case
            ExpressionAttributeValues={
                ":pk": {"S": item_id}  # Set the item_id value
            }
        )

        # Check if the item exists
        if 'Items' in response and response['Items']:
            item = response['Items'][0]  # Assuming the query returns one result
            # Convert Decimal values to float for easier manipulation
            for key, value in item.items():
                if isinstance(value, decimal.Decimal):
                    item[key] = float(value)

            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f"Item with ID {item_id} not found.")
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving item: {str(e)}")
        }
