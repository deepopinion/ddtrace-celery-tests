import logging
from os import environ

from celery import Celery


app = Celery('ddtrace-tests', broker=environ["REDIS_DSN"])
logging.basicConfig(level=environ["LOG_LEVEL"])
