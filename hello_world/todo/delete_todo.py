import boto3
import json
import os
import sys

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TODO_TABLE_NAME'])


def lambda_handler(event, context):
  todo_id = event['pathParameters']['id']
  table.delete_item(Key={'id': todo_id})

  return {
      'statusCode': 200,
      'body': None
  }
