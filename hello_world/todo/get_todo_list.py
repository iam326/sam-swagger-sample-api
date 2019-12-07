import boto3
import json
import os
import sys

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TODO_TABLE_NAME'])
index_name = os.environ['TODO_DATE_INDEX_NAME']


def lambda_handler(event, context):
  date = event['queryStringParameters']['date']
  response = table.query(IndexName=index_name,
                         KeyConditionExpression=Key('date').eq(date))

  return {
      'statusCode': 200,
      'body': json.dumps({
          'todo': response['Items']
      })
  }
