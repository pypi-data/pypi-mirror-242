# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205,W0613,R0801

import logging
from typing import Any, Dict
from pika.frame import Method
from pika.channel import Channel
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqQueue(RabbitmqChannel):
    def setup(self):
        super().setup()
        self.set("queue", self.get("queue", str))
        self.set("queue_passive", bool(self.get("queue_passive")))
        self.set("queue_durable", bool(self.get("queue_durable")))
        self.set("queue_exclusive", bool(self.get("queue_exclusive")))
        self.set("queue_auto_delete", bool(self.get("queue_auto_delete")))
        self.set("queue_arguments", dict(self.get("queue_arguments") or {}), dict)

    @property
    def queue(self) -> str:
        return self.get("queue", str)

    @property
    def queue_passive(self) -> bool:
        return bool(self.get("queue_passive"))

    @property
    def queue_durable(self) -> bool:
        return bool(self.get("queue_durable"))

    @property
    def queue_exclusive(self) -> bool:
        return bool(self.get("queue_exclusive"))

    @property
    def queue_auto_delete(self) -> bool:
        return bool(self.get("queue_auto_delete"))

    @property
    def queue_arguments(self) -> Dict[str, Any]:
        return self.get("queue_arguments", dict)


class RabbitmqQueueDeclare(RabbitmqQueue):
    _queue_is_declared: bool

    def __init__(self, **kwargs):
        self._queue_is_declared = False
        super().__init__(**kwargs)

    @property
    def is_declared_queue(self) -> bool:
        return bool(self._queue_is_declared)

    def waiting_declared_queue(self):
        while not self.is_declared_queue:
            continue
        return self

    def on_open_channel_ok(self):
        self.queue_declare()

    def queue_declare(self):
        LOGGER.info("Declaring queue: %s", self.queue)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.queue_declare(
                queue=self.queue,
                passive=self.queue_passive,
                durable=self.queue_durable,
                exclusive=self.queue_exclusive,
                auto_delete=self.queue_auto_delete,
                arguments=self.queue_arguments,
                callback=self.on_queue_declare_ok,
            )

    def on_queue_declare_ok(self, method_frame: Method):
        LOGGER.info("Queue declared: %s", self.queue)
        self.set("declared_queue", True)

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_declared_queue()


class RabbitmqQueueBind(RabbitmqQueue):
    _binded_queue: bool

    def __init__(self, **kwargs):
        self._binded_queue = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.set("queue_bind_exchange", self.get("queue_bind_exchange", str))
        self.set("queue_bind_arguments", dict(self.get("queue_bind_arguments") or {}))

    @property
    def is_binded_queue(self) -> int:
        return bool(self._binded_queue)

    @property
    def queue_bind_exchange(self) -> str:
        return self.get("queue_bind_exchange", str)

    @property
    def queue_bind_routing_key(self) -> str | None:
        return self.get("queue_bind_routing_key")

    @property
    def queue_bind_arguments(self) -> Dict[str, Any]:
        return self.get("queue_bind_arguments", dict)

    def waiting_binded_queue(self):
        while not self.is_binded_queue:
            continue
        return self

    def on_open_channel_ok(self):
        self.queue_bind()

    def queue_bind(self):
        LOGGER.info("Binding queue: %s", self.queue)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.queue_bind(
                queue=self.queue,
                exchange=self.queue_bind_exchange,
                routing_key=self.queue_bind_routing_key,
                arguments=self.queue_bind_arguments,
                callback=self.on_queue_bind_ok,
            )

    def on_queue_bind_ok(self, method_frame: Method):
        LOGGER.info("Queue binded: %s", self.queue)
        self.set("binded_queue", True)

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_binded_queue()
