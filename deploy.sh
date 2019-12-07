#!/bin/bash

set -euo pipefail

source ./config.sh

readonly BUCKET_NAME="iam326.${STACK_NAME}"

aws s3 cp swagger.yaml s3://${BUCKET_NAME}/swagger.yaml

sam build

sam package \
  --output-template-file packaged.yaml \
  --s3-bucket ${BUCKET_NAME}

sam deploy \
  --template-file packaged.yaml \
  --stack-name ${STACK_NAME} \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides \
    TodoTableName=${TODO_TABLE_NAME} \
    TodoDateIndexName=${TODO_DATE_INDEX_NAME}

rm packaged.yaml

readonly APIURL=$(aws cloudformation describe-stacks \
  --stack-name ${STACK_NAME} \
  --output text \
  --query 'Stacks[].Outputs[?OutputKey==`PythonVersionApiUrl`].OutputValue' \
)

echo ${APIURL}
