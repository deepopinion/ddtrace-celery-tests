import ddtrace
ddtrace.patch_all(celery=True)
ddtrace.patch(celery=True)

import logging
from os import environ

from celery import Celery


LOG_FORMAT = "[%(asctime)s %(levelname)s] %(message)s"


app = Celery('ddtrace-tests')
logging.basicConfig(level=environ["LOG_LEVEL"], format=LOG_FORMAT)
