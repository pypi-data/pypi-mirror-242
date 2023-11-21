import logging
from typing import Any, Callable
from confluent_kafka import Producer

from .classes import EventObject


def default_callback(err, msg):
    if err:
        logging.error("Message failed delivery: {}".format(err))


def produce(
    config: dict,
    logger: logging.Logger,
    topic: str,
    event_object: EventObject,
    callback: Callable = default_callback
):
    """Produce an event to the kafka message queue."""
    kafka_config = config["kafka.default"]
    kafka_config.update(config["kafka.producer"])

    producer = Producer(kafka_config)

    event_object.add_audit_log(config["general"]["current_location"])

    producer.produce(
        topic,
        key=str(event_object.correlation_id),
        value=event_object.encode(),
        callback=callback,
    )

    producer.poll(100)
    producer.flush()
