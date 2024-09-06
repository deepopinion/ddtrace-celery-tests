import logging

from ddtrace import tracer

from base import app

logger = logging.getLogger("worker")


@app.task()
def check():
    with tracer.trace("checking") as span:
        logger.info(
            "Worker got trace ID %s, span ID %s",
            span.trace_id, span.span_id
        )
        return {
            "worker_trace_id": span.trace_id,
            "worker_span_id": span.span_id,
        }
