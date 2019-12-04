import boto3
import json
import sys

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("sam-swagger-sample-todo")


def lambda_handler(event, context):

  result = table.query(IndexName="date-index",
                       KeyConditionExpression=Key("date").eq("2019-12-25"))

  return {
      "statusCode": 200,
      "body": json.dumps({
          "todo": result
      })
  }
