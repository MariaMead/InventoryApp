import json
import boto3
import uuid
from decimal import Decimal

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

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'item_id': unique_id,
                'item_name': data['item_name']['S'],
                'item_description': data['item_description']['S'],
                'item_qty': Decimal(data['item_qty']['N']),
                'item_price': Decimal(data['item_price']['N']),
                'item_location_id': Decimal(data['item_location_id']['N'])
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