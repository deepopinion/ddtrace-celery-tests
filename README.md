# ddtrace-celery-tests

Just a test repo to verify Celery with ddtrace

## Dependencies

These are the dependencies to run this example app:
* Python 3.9
* [Just](https://just.systems/)
* [Poetry](https://python-poetry.org/)
* [Docker Compose](https://docs.docker.com/compose/)

## Running

To run this example app and see the error:

```shell
$ just run
```

Notice how the traces and spans don't match between the producer and the consumer.
