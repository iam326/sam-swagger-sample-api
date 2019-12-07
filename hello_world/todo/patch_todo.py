import boto3
import json
import os
import sys

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TODO_TABLE_NAME'])


def lambda_handler(event, context):
  todo_id = event['pathParameters']['id']
  body = json.loads(event['body'])

  keys = []
  values = {}
  for k in body.keys():
    keys.append(f'{k} = :{k}')
    values[f':{k}'] = body[k]

  table.update_item(
      Key={'id': todo_id},
      UpdateExpression=f'set {", ".join(keys)}',
      ExpressionAttributeValues=values
  )

  return {
      'statusCode': 200,
      'body': None
  }
