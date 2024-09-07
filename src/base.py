import ddtrace


ddtrace.patch_all(langchain=False, logging=True)

import logging
import logging.config
from os import environ

from celery import Celery, signals
from ddtrace import tracer


LOG_FORMAT = (
    '[dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] - %(message)s'
)


def configure_logging() -> Celery:

    app = Celery('ddtrace-tests')
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "root": {
            "level": environ["LOG_LEVEL"],
            "handlers": ["default"],
        },
        "loggers": {
            "ddtrace-celery-tests": {"propagate": True},
        },
    })

    return app


app = configure_logging()

logger = logging.getLogger("ddtrace-celery-tests.base")


def debug_trace():
    trace_id = tracer.current_span().trace_id
    span_id = tracer.current_span().span_id
    logger.info("trace_id, span_id: %s, %s", trace_id, span_id)
    logger.info("Enabled? %s", tracer.enabled)
    logger.info("Correlation context: %s",
                tracer.get_log_correlation_context())
    logger.info("Agent URL: %s", tracer.agent_trace_url)


@signals.setup_logging.connect
def on_setup_logging(**kwargs):
    configure_logging()
