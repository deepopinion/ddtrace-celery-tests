from ddtrace import patch_all; patch_all()

import time
import logging

from ddtrace import tracer

from worker import check


SLEEP_TIME = 3
LOG_FORMAT = "[%(asctime)s %(levelname)s] %(message)s"

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("nagger")


def nag():
    try:
        while True:
            with tracer.trace("nagging") as span:
                logger.info(
                    "Nagger got trace ID %s, span ID %s",
                    span.trace_id, span.span_id
                )
                check.delay()
                time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        exit("Exiting...")


if __name__ == "__main__":
    nag()
