import time
import logging

from ddtrace import tracer

from base import debug_trace
from worker import check


SLEEP_TIME = 10

logger = logging.getLogger("ddtrace-celery-tests.nagger")


def nag():
    try:
        while True:
            logger.info("***** Starting new nag *****")
            with tracer.trace("nagging") as span:
                debug_trace()
                time.sleep(0.1)
                async_task = check.apply_async()
                time.sleep(0.1)
                result = async_task.get()
                logger.info("Got result from worker: %s", result)
                logger.info(
                    "Nagger got trace ID %s, span ID %s",
                    span.trace_id, span.span_id
                )
                if span.trace_id == result["worker_trace_id"]:
                    logger.info("Traces match! :-)")
                else:
                    logger.warning("Traces don't match... :-(")
                if span.span_id == result["worker_span_id"]:
                    logger.info("Spans match! :-)")
                else:
                    logger.warning("Spans don't match... :-(")
            logger.info("***** Finished nag *****")
            logging.getLogger().handlers[0].flush()
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        exit("Exiting...")


if __name__ == "__main__":
    nag()
