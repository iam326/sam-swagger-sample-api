#!/bin/bash

set -euo pipefail

source ./config.sh

python -m pytest tests/api/ -v -s
