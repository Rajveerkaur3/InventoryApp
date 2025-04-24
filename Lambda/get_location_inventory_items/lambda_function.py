import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'Inventory'
GSI_NAME = 'GSI_LocationIndex'  # Use the correct GSI name

def convert_decimals(obj):
    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):  
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)

    try:
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                'statusCode': 400,
                'body': json.dumps("Missing 'id' path parameter")
            }
        
        location_id_value = int(event['pathParameters']['id'])

        # Correct the partition key name to 'item_location_id'
        response = table.query(
            IndexName=GSI_NAME,
            KeyConditionExpression=Key('item_location_id').eq(location_id_value)
        )
        items = response.get('Items', [])

        items = convert_decimals(items)
    except ClientError as e:
        print(f"Failed to query items: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Failed to query items')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(items)
    }
