import boto3
import os
import requests

import pytest

cognito = boto3.client('cognito-idp')
apigateway = boto3.client('apigateway')


def get_user_pool(user_pool_name):
  response = cognito.list_user_pools(
      MaxResults=10
  )
  for user_pool in response['UserPools']:
    if user_pool['Name'] == user_pool_name:
      return user_pool

  return None


def get_user_pool_client(user_pool_id, client_name):
  response = cognito.list_user_pool_clients(
      UserPoolId=user_pool_id,
      MaxResults=10
  )
  for user_pool_client in response['UserPoolClients']:
    if user_pool_client['ClientName'] == client_name:
      return user_pool_client

  return None


def get_user_pool_client_id_token(user_pool_client_id, username, password):
  response = cognito.initiate_auth(
      AuthFlow='USER_PASSWORD_AUTH',
      AuthParameters={
          'USERNAME': username,
          'PASSWORD': password
      },
      ClientId=user_pool_client_id
  )
  return response['AuthenticationResult']['IdToken']


def get_rest_api(api_name):
  response = apigateway.get_rest_apis()
  for api in response['items']:
    if api['name'] == api_name:
      return api

  return None


@pytest.fixture
def init():
  username = os.environ['SAM_SWAGGER_SAMPLE_USERNAME']
  password = os.environ['SAM_SWAGGER_SAMPLE_PASSWORD']

  user_pool = get_user_pool('sam-swagger-sample-user-pool')

  user_pool_client = get_user_pool_client(
      user_pool['Id'], 'sam-swagger-sample-user-pool-client')

  id_token = get_user_pool_client_id_token(
      user_pool_client['ClientId'], username, password)

  api = get_rest_api('Sample API')
  base_url = f"https://{api['id']}.execute-api.ap-northeast-1.amazonaws.com/Prod"

  headers = {
      'Authorization': id_token
  }

  return base_url, headers


def test_get_python_version(init):
  base_url = init[0]
  headers = init[1]
  response = requests.get(f"{base_url}/version", headers=headers)
  body = response.json()

  assert response.status_code == 200
  assert 'python' in body
  assert body['python'] == '3.7.5'
