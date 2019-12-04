import boto3
import json
import sys

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("sam-swagger-sample-todo")


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
