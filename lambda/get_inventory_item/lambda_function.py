import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = 'Inventory'

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    # Get the key from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']
    
    try: 
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )
        items = response.get('Items', [])
   
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
    
        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)  # Use str to handle any special types like Decimal
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }