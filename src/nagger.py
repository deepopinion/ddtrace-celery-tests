import time
import logging

from ddtrace import tracer

from worker import check


SLEEP_TIME = 3

logger = logging.getLogger("nagger")


def nag():
    try:
        while True:
            with tracer.trace("nagging") as span:
                async_task = check.delay()
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
                time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        exit("Exiting...")


if __name__ == "__main__":
    nag()
