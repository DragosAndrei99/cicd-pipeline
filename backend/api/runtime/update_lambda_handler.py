import os
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    item_key = event.get('item_key')
    update_data = event.get('update_data')

    if not item_key or not update_data:
        return {
            'statusCode': 400,
            'body': 'Item key or update data not provided in the event'
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)

    try:
        response = table.update_item(
            Key=item_key,
            UpdateExpression='SET title = :val1',
            ExpressionAttributeValues={
                ':val1': update_data['title'],
            }
        )

        return {
            'statusCode': 200,
            'body': 'Item updated successfully',
            'response': response
        }

    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': 'Error updating item in DynamoDB',
            'error_message': e.response['Error']['Message']
        }
