#!/bin/bash

set -euo pipefail

source ./config.sh

readonly USERNAME=$1
readonly EMAIL=$2
readonly PASSWORD=$3

readonly USER_POOL_ID=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --output text \
  --query 'Stacks[].Outputs[?OutputKey==`UserPoolId`].OutputValue' \
)

readonly USER_POOL_CLIENT_ID=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --output text \
  --query 'Stacks[].Outputs[?OutputKey==`UserPoolClientId`].OutputValue' \
)

USER=$(aws cognito-idp admin-create-user \
  --user-pool-id ${USER_POOL_ID} \
  --username ${USERNAME} \
  --user-attributes Name=email,Value=${EMAIL} \
  --temporary-password=${PASSWORD} \
  --message-action=SUPPRESS
)

AUTH_CHALLENGE_SESSION=$(aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id ${USER_POOL_CLIENT_ID} \
  --auth-parameters "USERNAME=${USERNAME},PASSWORD=${PASSWORD}" \
  --query "Session" \
  --output text
)

AUTH_TOKEN=$(aws cognito-idp respond-to-auth-challenge \
  --client-id ${USER_POOL_CLIENT_ID} \
  --challenge-responses "NEW_PASSWORD=${PASSWORD},USERNAME=${USERNAME}" \
  --challenge-name NEW_PASSWORD_REQUIRED \
  --session ${AUTH_CHALLENGE_SESSION} \
  --query "AuthenticationResult.IdToken" \
  --output text
)

echo ${AUTH_TOKEN}
