import json

import pytest

from hello_world import app
from hello_world.todo import get_todo_list
from hello_world.todo import get_todo
from hello_world.todo import post_todo
from hello_world.todo import patch_todo
from hello_world.todo import delete_todo


@pytest.fixture()
def apigw_event():
  """ Generates API GW Event"""

  return {
      "body": '{ "test": "body"}',
      "resource": "/{proxy+}",
      "requestContext": {
          "resourceId": "123456",
          "apiId": "1234567890",
          "resourcePath": "/{proxy+}",
          "httpMethod": "POST",
          "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
          "accountId": "123456789012",
          "identity": {
              "apiKey": "",
              "userArn": "",
              "cognitoAuthenticationType": "",
              "caller": "",
              "userAgent": "Custom User Agent String",
              "user": "",
              "cognitoIdentityPoolId": "",
              "cognitoIdentityId": "",
              "cognitoAuthenticationProvider": "",
              "sourceIp": "127.0.0.1",
              "accountId": "",
          },
          "stage": "prod",
      },
      "queryStringParameters": {"foo": "bar"},
      "headers": {
          "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
          "Accept-Language": "en-US,en;q=0.8",
          "CloudFront-Is-Desktop-Viewer": "true",
          "CloudFront-Is-SmartTV-Viewer": "false",
          "CloudFront-Is-Mobile-Viewer": "false",
          "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
          "CloudFront-Viewer-Country": "US",
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Upgrade-Insecure-Requests": "1",
          "X-Forwarded-Port": "443",
          "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
          "X-Forwarded-Proto": "https",
          "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
          "CloudFront-Is-Tablet-Viewer": "false",
          "Cache-Control": "max-age=0",
          "User-Agent": "Custom User Agent String",
          "CloudFront-Forwarded-Proto": "https",
          "Accept-Encoding": "gzip, deflate, sdch",
      },
      "pathParameters": {"proxy": "/examplepath"},
      "httpMethod": "POST",
      "stageVariables": {"baz": "qux"},
      "path": "/examplepath",
  }


def test_lambda_handler(apigw_event, mocker):

  response = app.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert "python" in response["body"]
  assert data["python"] == "3.7.5"


def test_get_todo_list(apigw_event, mocker):

  response = get_todo_list.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert "todo" in response["body"]
  assert data["todo"] == [{}, {}]


def test_get_todo(apigw_event, mocker):

  response = get_todo.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert "todo" in response["body"]
  assert data["todo"] == [{}]


def test_post_todo(apigw_event, mocker):

  response = post_todo.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert data == {}


def test_patch_todo(apigw_event, mocker):

  response = patch_todo.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert data == {}


def test_delete_todo(apigw_event, mocker):

  response = delete_todo.lambda_handler(apigw_event, "")
  data = json.loads(response["body"])

  assert response["statusCode"] == 200
  assert data == {}
