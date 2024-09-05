import logging

from ddtrace import tracer
from ddtrace.context import Context

from base import app

logger = logging.getLogger("worker")

@app.task(bind=True)
def check(self):
    headers = self.request.headers
    tracer.context_provider.activate(Context(
        trace_id=headers["trace_id"],
        span_id=headers["span_id"],
    ))
    with tracer.trace("checking") as span:
        logger.info(
            "Worker got trace ID %s, span ID %s",
            span.trace_id, span.span_id
        )
        return {
            "worker_trace_id": span.trace_id,
            "worker_span_id": span.span_id,
        }
