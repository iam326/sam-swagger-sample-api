import json
import sys


def lambda_handler(event, context):

  version = f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'
  return {
      "statusCode": 200,
      "body": json.dumps({
          "python": version
      })
  }
