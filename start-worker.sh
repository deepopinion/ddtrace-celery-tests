#!/usr/bin/env bash

poetry run celery -A worker worker --loglevel="${LOG_LEVEL}" --concurrency=1 -n worker1
