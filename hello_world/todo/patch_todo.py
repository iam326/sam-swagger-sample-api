import boto3
import json
import sys

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("sam-swagger-sample-todo")


def lambda_handler(event, context):

  table.update_item(
      Key={
          "id": "hoge"
      },
      UpdateExpression="set title = :title",
      ExpressionAttributeValues={
          ":title": "title2"
      }
  )

  return {
      "statusCode": 200,
      "body": json.dumps({})
  }
