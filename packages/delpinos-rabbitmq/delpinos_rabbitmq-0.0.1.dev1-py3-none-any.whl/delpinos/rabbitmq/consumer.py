# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,W0640,R0801

import json
import logging
import threading
from typing import Any, Dict, List, Type
from pika.channel import Channel
from pika.spec import BasicProperties, Basic
from delpinos.core.factories.factory import Factory
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqConsumer(RabbitmqChannel):
    _closing: bool
    _consuming: bool
    _consumer_tag: str | None
    _qos_is_seted: bool

    def __init__(self, **kwargs):
        self._closing = False
        self._consuming = False
        self._consumer_tag = None
        self._qos_is_seted = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        consumer_queue = self.get("consumer_queue", str)
        self.set("consumer_queue", consumer_queue)
        self.set("consumer_retries", int(self.get("consumer_retries") or 0))
        self.set("consumer_prefetch_size", int(self.get("consumer_prefetch_size") or 0))
        self.set(
            "consumer_prefetch_count", int(self.get("consumer_prefetch_count") or 1)
        )
        self.set("consumer_global_qos", bool(self.get("consumer_global_qos")))
        self.set("consumer_dlq_enable", bool(self.get("consumer_dlq_enable")))
        self.set(
            "consumer_dlq_exceptions",
            self.get("consumer_dlq_exceptions") or [json.JSONDecodeError],
        )
        self.set("consumer_dlq_enable", bool(self.get("consumer_dlq_enable")))
        self.set(
            "consumer_dlq_exchange", self.get("consumer_dlq_exchange") or "default"
        )
        self.set(
            "consumer_dlq_routing_key",
            self.get("consumer_dlq_routing_key") or consumer_queue + ".dlq",
        )
        self.set("consumer_header_retry", self.get("consumer_header_retry") or "retry")
        self.set(
            "consumer_header_exception",
            self.get("consumer_header_exception") or "exception",
        )

    @property
    def consumer_queue(self) -> str:
        return self.get("consumer_queue", str)

    @property
    def consumer_header_retry(self) -> str:
        return self.get("consumer_header_retry", str)

    @property
    def consumer_header_exception(self) -> str:
        return self.get("consumer_header_exception", str)

    @property
    def consumer_retries(self) -> int:
        return self.get("consumer_retries", int)

    @property
    def consumer_prefetch_size(self) -> int:
        return self.get("consumer_prefetch_size", int)

    @property
    def consumer_prefetch_count(self) -> int:
        return self.get("consumer_prefetch_count", int)

    @property
    def consumer_global_qos(self) -> bool:
        return self.get("consumer_global_qos", bool)

    @property
    def consumer_dlq_enable(self) -> bool:
        return self.get("consumer_dlq_enable", bool)

    @property
    def consumer_dlq_exceptions(self) -> List[Type[Exception]]:
        return self.get("consumer_dlq_exceptions", list)

    @property
    def consumer_dlq_exchange(self) -> str:
        return self.get("consumer_dlq_exchange")

    @property
    def consumer_dlq_routing_key(self) -> str:
        return self.get("consumer_dlq_routing_key")

    @property
    def qos_is_seted(self) -> int:
        return self._qos_is_seted

    def waiting_qos_is_seted(self):
        while not self.qos_is_seted:
            continue
        return self

    def on_open_channel_ok(self):
        self.set_qos()

    def consume(
        self,
        queue=None,
        exclusive=None,
        consumer_tag=None,
        arguments=None,
        callback=None,
    ):
        callback = self.default_on_event_ok if not callable(callback) else callback
        return self.basic_consume(
            queue=queue or self.consumer_queue,
            on_message_callback=self.consume_message,
            auto_ack=False,
            exclusive=exclusive,
            consumer_tag=consumer_tag,
            arguments=arguments,
            callback=callback,
        )

    def check_message_retry(
        self, properties: BasicProperties, body: bytes, err: Exception
    ) -> bool:
        try:
            for exception_class in list(self.consumer_dlq_exceptions):
                if isinstance(exception_class, type) and isinstance(
                    err, exception_class
                ):
                    return False
            headers = properties.headers or {}
            retry = int(headers.get(self.consumer_header_retry) or 0) + 1
            retries = self.consumer_retries
            if retry > retries:
                return False
        except Exception:
            return False
        return True

    def consume_message(
        self,
        channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        try:
            self.on_message(channel, basic_deliver, properties, body)
            self.on_message_ok(channel, basic_deliver, properties, body)
        except Exception as err:
            if self.check_message_retry(properties, body, err):
                self.on_message_retry(channel, basic_deliver, properties, body, err)
            else:
                self.on_message_error(channel, basic_deliver, properties, body, err)

    def on_message(
        self,
        channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        LOGGER.warn("%s", body)

    def on_message_ok(
        self,
        channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)

    def on_message_retry(
        self,
        channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        err: Exception,
    ):
        try:
            headers = dict(properties.headers or {})
            headers[self.consumer_header_retry] = (
                int(headers.get(self.consumer_header_retry) or 0) + 1
            )
            headers[self.consumer_header_exception] = dict(
                type=f"{err.__class__.__module__}.{err.__class__.__name__}",
                message=str(err),
            )
            properties.headers = headers
            self.basic_publish(
                exchange=basic_deliver.exchange,
                routing_key=basic_deliver.routing_key,
                properties=properties,
                body=body,
            )
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
        except Exception:
            channel.basic_reject(delivery_tag=basic_deliver.delivery_tag)

    def on_message_error(
        self,
        channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
        err: Exception,
    ):
        try:
            if self.consumer_dlq_enable:
                headers = dict(properties.headers or {})
                headers[self.consumer_header_exception] = dict(
                    type=f"{err.__class__.__module__}.{err.__class__.__name__}",
                    message=str(err),
                )
                properties.headers = headers
                self.basic_publish(
                    exchange=self.consumer_dlq_exchange,
                    routing_key=self.consumer_dlq_routing_key,
                    properties=properties,
                    body=body,
                )
                channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
            else:
                raise Exception()
        except Exception:
            channel.basic_reject(delivery_tag=basic_deliver.delivery_tag)

    def set_qos(self):
        self.basic_qos(
            prefetch_size=self.consumer_prefetch_size,
            prefetch_count=self.consumer_prefetch_count,
            global_qos=self.consumer_global_qos,
            callback=self.on_basic_qos_ok,
        )

    def on_basic_qos_ok(self, method_frame):
        self._qos_is_seted = True
        self.start_consuming()

    def start_consuming(self):
        LOGGER.warn("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self.consume(queue=self.consumer_queue)
        self._consuming = True

    def add_on_cancel_callback(self):
        LOGGER.warn("Adding consumer cancellation callback")
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.add_on_cancel_callback(self.on_cancel_consumer_ok)

    def stop_consuming(self):
        if isinstance(self.channel, Channel):
            LOGGER.warn("Sending a Basic.Cancel RPC command to RabbitMQ")
            self.basic_cancel(
                consumer_tag=self._consumer_tag, callback=self.on_cancel_consumer_ok
            )

    def on_cancel_consumer_ok(self, method_frame):
        LOGGER.warn(
            "RabbitMQ acknowledged the cancellation of the consumer: %s",
            self._consumer_tag,
        )
        self._consuming = False
        self.close_channel()

    def health_check(self) -> tuple:
        try:
            health_check = super().health_check()
            if not isinstance(health_check, tuple):
                raise Exception("Unhealth")
            if not health_check[0]:
                return health_check
            if not self.is_running_connection:
                raise Exception("Rabbitmq consumer is not running")
            if self.is_closing_connection:
                raise Exception("Rabbitmq consumer is closing")
            return True, "Success"
        except Exception as err:
            return False, str(err)

    def stop(self, blocking: bool = True):
        if not self._closing:
            self._closing = True
            LOGGER.warn("Stopping consumer")
            if self._consuming:
                self.stop_consuming()
            LOGGER.warn("Consumer Stopped")

        super().stop(blocking)

    def run(self, blocking: bool = True):
        super().run(blocking)
        if blocking:
            self.waiting_qos_is_seted()


class RabbitmqJsonConsumer(RabbitmqConsumer):
    def setup(self):
        super().setup()
        self.consumer_dlq_exceptions.append(json.JSONDecodeError)

    def decode_message(self, body: bytes) -> Dict[str, Any]:
        return dict(json.loads(body))


class RabbitmqConsumerMultiple(Factory):
    _instances: int
    _consumers: List[RabbitmqConsumer]
    _threads: List[threading.Thread]
    _consumer_class: Type[RabbitmqConsumer]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._consumer_class = self.get("consumer_class") or RabbitmqConsumer
        self._instances = int(kwargs.get("instances", 1) or 1)
        self._consumers = []
        self._threads = []

    @property
    def threads(self) -> List[threading.Thread]:
        return self._threads

    @property
    def consumers(self) -> List[RabbitmqConsumer]:
        return self._consumers

    def add_consumer(self, number: int = 1, blocking: bool = False):
        number = number or 1
        LOGGER.warn("Adding Consumer %i", number or 1)
        consumer = None
        try:
            consumer = self._consumer_class(**self.kwargs())
            self._consumers.append(consumer)
            LOGGER.warn("Starting Consumer %i", number or 1)
            consumer.run(blocking=blocking)
            LOGGER.warn("Added Consumer %i", number or 1)
        except Exception as err:
            LOGGER.error(err)
            consumer = None

    def health_check(self) -> tuple:
        try:
            errors = []
            consumer_number = 0
            for consumer in self.consumers:
                try:
                    consumer_number += 1
                    health_check = consumer.health_check()
                    if not isinstance(health_check, tuple):
                        raise Exception("Unhealth")
                    if not health_check[0]:
                        raise Exception(health_check[1])
                except Exception as err:
                    errors.append(f"Consumer {consumer_number}: {err}")
            if len(errors) > 0:
                return False, ", ".join(errors)
            return True, "Success"
        except Exception as err:
            return False, str(err)

    def run(self, blocking: bool = False):
        for i in range(0, self._instances):
            thread = threading.Thread(
                target=lambda: self.add_consumer(i + 1, blocking), daemon=True
            )
            thread.start()
            self._threads.append(thread)

    def stop(self, blocking: bool = False):
        for consumer in self.consumers:
            consumer.stop(blocking)
