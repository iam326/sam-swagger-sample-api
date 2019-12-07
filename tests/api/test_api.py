import boto3
import json
import os
import requests

import pytest

cognito = boto3.client('cognito-idp')
apigateway = boto3.client('apigateway')
todo_ids = []


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


@pytest.fixture(scope='session', autouse=True)
def setup():
  username = os.environ['SAM_SWAGGER_SAMPLE_USERNAME']
  password = os.environ['SAM_SWAGGER_SAMPLE_PASSWORD']

  user_pool = get_user_pool('sam-swagger-sample-user-pool')

  user_pool_client = get_user_pool_client(
      user_pool['Id'], 'sam-swagger-sample-user-pool-client')

  id_token = get_user_pool_client_id_token(
      user_pool_client['ClientId'], username, password)

  api = get_rest_api('Sample API')
  base_url = f'https://{api["id"]}.execute-api.ap-northeast-1.amazonaws.com/Prod'

  headers = {
      'Authorization': id_token,
      'Content-type': 'application/json'
  }

  return base_url, headers


def test_get_python_version(setup):
  base_url = setup[0]
  headers = setup[1]
  response = requests.get(f'{base_url}/version', headers=headers)
  body = response.json()

  assert response.status_code == 200
  assert 'python' in body
  assert body['python'] == '3.7.5'


def test_post_todo(setup):
  base_url = setup[0]
  headers = setup[1]
  data = json.dumps({
      'date': '2019-12-25',
      'title': 'dummy_title',
      'body': 'dummy_body'
  }).encode('utf-8')

  response1 = requests.post(f'{base_url}/todo', headers=headers, data=data)
  response2 = requests.post(f'{base_url}/todo', headers=headers, data=data)
  todo = response1.json()['todo']

  assert response1.status_code == 200
  assert len(todo) == 1
  assert 'id' in todo[0]
  assert type(todo[0]['id']) == str

  global todo_ids
  todo_ids.append(todo[0]['id'])
  todo_ids.append(response2.json()['todo'][0]['id'])


def test_get_todo(setup):
  base_url = setup[0]
  headers = setup[1]

  response = requests.get(f'{base_url}/todo/{todo_ids[0]}', headers=headers)
  todo = response.json()['todo']

  assert response.status_code == 200
  assert len(todo) == 1
  assert 'id' in todo[0]
  assert todo[0]['id'] == todo_ids[0]


def test_get_todo_list(setup):
  base_url = setup[0]
  headers = setup[1]
  params = {'date': '2019-12-25'}

  response = requests.get(f'{base_url}/todo', headers=headers, params=params)
  todo = response.json()['todo']

  assert response.status_code == 200
  assert len(todo) == 2


def test_patch_todo(setup):
  base_url = setup[0]
  headers = setup[1]
  data = json.dumps({
      'title': 'dummy_title_patched',
      'body': 'dummy_body_patched'
  }).encode('utf-8')

  requests.patch(
      f'{base_url}/todo/{todo_ids[0]}', headers=headers, data=data)

  response = requests.get(f'{base_url}/todo/{todo_ids[0]}', headers=headers)
  todo = response.json()['todo']
  item = todo[0]

  assert response.status_code == 200
  assert len(todo) == 1
  assert 'id' in item
  assert item['id'] == todo_ids[0]
  assert 'title' in item
  assert item['title'] == 'dummy_title_patched'
  assert 'body' in item
  assert item['body'] == 'dummy_body_patched'


def test_delete_todo(setup):
  base_url = setup[0]
  headers = setup[1]

  response = requests.delete(f'{base_url}/todo/{todo_ids[0]}', headers=headers)
  requests.delete(f'{base_url}/todo/{todo_ids[1]}', headers=headers)

  assert response.status_code == 200
