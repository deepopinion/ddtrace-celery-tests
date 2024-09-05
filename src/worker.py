import logging

from celery.signals import before_task_publish, task_prerun
from ddtrace import tracer
from ddtrace.context import Context

from base import app

logger = logging.getLogger("worker")


@before_task_publish.connect
def propagate_context(sender=None, headers=None, body=None, **kwargs):
    span = tracer.current_span()
    headers["trace_id"] = span.trace_id
    headers["span_id"] = span.span_id


@task_prerun.connect
def hydrate_context(task_id=None, task=None, *args, **kwargs):
    tracer.context_provider.activate(Context(
        trace_id=task.request.headers["trace_id"],
        span_id=task.request.headers["span_id"],
    ))


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
