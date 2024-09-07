import logging
import time

from ddtrace import tracer

from base import app, debug_trace


logger = logging.getLogger("ddtrace-celery-tests.worker")


@app.task(bind=True)
def check(self):
    time.sleep(0.1)
    logger.info("Bound headers: %s", self.request.headers)
    debug_trace()
    with tracer.trace("checking") as span:
        logger.info(
            "Worker got trace ID %s, span ID %s",
            span.trace_id, span.span_id
        )
        logging.getLogger().handlers[0].flush()
        time.sleep(1)
        return {
            "worker_trace_id": span.trace_id,
            "worker_span_id": span.span_id,
        }
