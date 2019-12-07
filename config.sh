#!/bin/bash

set -euo pipefail

readonly STACK_NAME="sam-swagger-sample"
export TODO_TABLE_NAME=${STACK_NAME}-todo
export TODO_DATE_INDEX_NAME="date-index"
