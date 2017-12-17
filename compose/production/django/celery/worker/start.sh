#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


celery -A interface_blockchain.taskapp worker -l INFO
