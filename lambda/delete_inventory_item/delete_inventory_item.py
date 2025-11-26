import boto3
import json
from boto3.dynamodb.conditions import Key



def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'Inventory'

    table = dynamodb.Table(table_name)

    # Extract the '_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # Attempt to delete the item from the table
    try:
        response = table.query(
            KeyConditionExpression=Key('item_id').eq(item_id)
        )
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }
        for item in items:
            item_location_id = item['item_location_id']
            table.delete_item(
                Key={
                    'item_id': item_id,
                    'item_location_id': item_location_id
                }
            )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }