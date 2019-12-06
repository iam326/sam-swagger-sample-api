import boto3
import json
import os
import sys

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TODO_TABLE_NAME"])


def lambda_handler(event, context):

  table.delete_item(
      Key={
          "id": "hoge"
      }
  )

  return {
      "statusCode": 200,
      "body": json.dumps({})
  }
