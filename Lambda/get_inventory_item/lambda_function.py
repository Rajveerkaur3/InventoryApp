import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
    # DynamoDB setup
    dynamodb = boto3.client('dynamodb')  # Note: using client for query()
    table_name = 'Inventory'

    # Retrieve item_id from the pathParameters
    item_id = event['pathParameters']['id']

    try:
        # Query DynamoDB using only the partition key
        response = dynamodb.query(
            TableName=table_name,
            KeyConditionExpression='item_id = :item_id',
            ExpressionAttributeValues={
                ':item_id': {'S': item_id}
            }
        )

        items = response.get('Items', [])

        if items:
            # Convert DynamoDB types to standard Python types
            def deserialize(d):
                return {
                    k: float(v['N']) if 'N' in v else v.get('S', '')
                    for k, v in d.items() if k != 'item_location_id'
                }

            cleaned_items = [deserialize(item) for item in items]

            return {
                'statusCode': 200,
                'body': json.dumps(cleaned_items)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f"No items found with ID {item_id}.")
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error retrieving item: {str(e)}")
        }
