import boto3
import json
import os
import sys
# import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TODO_TABLE_NAME"])


def lambda_handler(event, context):

  table.put_item(
      Item={
          # "id": str(uuid.uuid4()),
          "id": "hoge",
          "date": "2019-12-25",
          "title": "foo",
          "body": "bar"
      }
  )

  return {
      "statusCode": 200,
      "body": json.dumps({})
  }
