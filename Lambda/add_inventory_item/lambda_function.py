
import json
import uuid
from decimal import Decimal

import boto3

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Inventory')

    # Generate a unique ID
    unique_id = str(uuid.uuid4())

    # Convert item_price to Decimal
    item_price = Decimal(str(data['item_price']))  # Ensure it's a valid Decimal

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'item_name': data['item_name'],
                'item_description': data['item_description'],
                'item_qty_on_hand': data['item_qty_on_hand'],
                'item_price': item_price,
                'item_location_id': data['item_location_id']
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }
