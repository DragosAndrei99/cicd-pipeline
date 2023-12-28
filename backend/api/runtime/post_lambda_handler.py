import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    item_data = event.get('item_data')
    if not item_data:
        return {
            'statusCode': 400,
            'body': 'Item data not provided in the event'
        }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)

    try:
        response = table.put_item(Item=item_data)

        return {
            'statusCode': 200,
            'body': 'Item created successfully',
            'response': response
        }

    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': 'Error creating item in DynamoDB',
            'error_message': e.response['Error']['Message']
        }
