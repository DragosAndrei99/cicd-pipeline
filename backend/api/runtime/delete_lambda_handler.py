import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    item_key = event.get('item_key')

    if not item_key:
        return {
            'statusCode': 400,
            'body': 'Item key not provided in the event'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)
    try:
        response = table.delete_item(Key=item_key)

        return {
            'statusCode': 200,
            'body': 'Item deleted successfully',
            'response': response
        }

    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': 'Error deleting item from DynamoDB',
            'error_message': e.response['Error']['Message']
        }
