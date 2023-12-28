import os
import json
import boto3
from botocore.exceptions import ClientError

def get_items_dynamodb(event, context):
    dynamodb_table_name = os.environ.get("DYNAMODB_TABLE_NAME")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(dynamodb_table_name)

    try:
        response = table.scan()
        items = response.get('Items', [])
        items_json = json.dumps(items, default=str)

        return {
            'statusCode': 200,
            'body': items_json
        }

    except ClientError as e:
        print(f"Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': 'Error retrieving items from DynamoDB'
        }

