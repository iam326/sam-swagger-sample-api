import boto3
import json
import os
import sys
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TODO_TABLE_NAME'])


def lambda_handler(event, context):
  body = json.loads(event['body'])
  item = {
      'id': str(uuid.uuid4()),
      'date': body['date'],
      'title': body['title'],
      'body': body['body']
  }
  table.put_item(Item=item)

  return {
      'statusCode': 200,
      'body': json.dumps({
          'todo': [item]
      })
  }
