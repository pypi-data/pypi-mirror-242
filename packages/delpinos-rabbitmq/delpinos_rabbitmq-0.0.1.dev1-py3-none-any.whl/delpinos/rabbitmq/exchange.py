# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
from typing import Any, Dict
from pika.channel import Channel
from pika.frame import Method
from pika.exchange_type import ExchangeType
from .channel import RabbitmqChannel

LOGGER = logging.getLogger(__name__)


class RabbitmqExchange(RabbitmqChannel):
    def setup(self):
        super().setup()
        self.set("exchange", self.get("exchange", str))
        self.set("exchange_type", str(self.get("exchange_type") or ExchangeType.topic))
        self.set("exchange_passive", bool(self.get("exchange_passive")))
        self.set("exchange_durable", bool(self.get("exchange_durable")))
        self.set("exchange_auto_delete", bool(self.get("exchange_auto_delete")))
        self.set("exchange_internal", bool(self.get("exchange_internal")))
        self.set("exchange_arguments", dict(self.get("exchange_arguments") or {}), dict)

    @property
    def exchange(self) -> str:
        return self.get("exchange", str)

    @property
    def exchange_type(self) -> str:
        return self.get("exchange_type", str)

    @property
    def exchange_passive(self) -> bool:
        return self.get("exchange_passive", bool)

    @property
    def exchange_durable(self) -> bool:
        return self.get("exchange_durable", bool)

    @property
    def exchange_auto_delete(self) -> bool:
        return self.get("exchange_auto_delete", bool)

    @property
    def exchange_internal(self) -> bool:
        return self.get("exchange_internal", bool)

    @property
    def exchange_arguments(self) -> Dict[str, Any]:
        return self.get("exchange_arguments", dict)


class RabbitmqExchangeDeclare(RabbitmqExchange):
    _exchange_is_declared: bool

    def __init__(self, **kwargs):
        self._exchange_is_declared = False
        super().__init__(**kwargs)

    @property
    def exchange_is_declared(self) -> int:
        return self._exchange_is_declared

    def waiting_exchange_is_declared(self):
        while not self.exchange_is_declared:
            continue
        return self

    def on_open_channel_ok(self):
        self.exchange_declare()

    def exchange_declare(self):
        """Setup the exchange on RabbitMQ by invoking the Exchange.Declare RPC
        command. When it is complete, the on_exchange_declare_ok method will
        be invoked by pika.
        """

        LOGGER.info("Declaring exchange: %s", self.exchange)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.exchange_declare(
                exchange=self.exchange,
                exchange_type=self.exchange_type,
                passive=self.exchange_passive,
                durable=self.exchange_durable,
                auto_delete=self.exchange_auto_delete,
                internal=self.exchange_internal,
                arguments=self.exchange_arguments,
                callback=self.on_exchange_declare_ok,
            )

    def on_exchange_declare_ok(self, method_frame: Method):
        """Invoked by pika when RabbitMQ has finished the Exchange.Declare RPC
        command.

        :param pika.Frame.Method unused_frame: Exchange.DeclareOk response frame
        :param dict: Config

        """
        LOGGER.info("Exchange declared: %s", self.exchange)
        self._exchange_is_declared = True

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_declared()


class RabbitmqExchangeBind(RabbitmqExchange):
    _exchange_is_binded: bool

    def __init__(self, **kwargs):
        self._exchange_is_binded = False
        super().__init__(**kwargs)

    def setup(self):
        super().setup()
        self.set(
            "exchange_bind_routing_key", self.get("exchange_bind_routing_key") or ""
        )
        self.set(
            "exchange_bind_destination", self.get("exchange_bind_destination", str)
        )
        self.set("exchange_bind_source", self.get("exchange_bind_source", str))
        self.set(
            "exchange_bind_arguments", dict(self.get("exchange_bind_arguments") or {})
        )

    @property
    def exchange_is_binded(self) -> int:
        return self._exchange_is_binded

    @property
    def exchange_bind_routing_key(self) -> str:
        return self.get("exchange_bind_routing_key", str)

    @property
    def exchange_bind_destination(self) -> str:
        return self.get("exchange_bind_destination", str)

    @property
    def exchange_bind_source(self) -> str:
        return self.get("exchange_bind_source", str)

    @property
    def exchange_bind_arguments(self) -> Dict[str, Any]:
        return self.get("exchange_bind_arguments", dict)

    def waiting_exchange_is_binded(self):
        while not self.exchange_is_binded:
            continue
        return self

    def on_open_channel_ok(self):
        self.exchange_bind()

    def exchange_bind(self):
        """Setup the exchange bind on RabbitMQ. When it is complete, the on_exchange_bind_ok method will
        be invoked by pika.
        """

        LOGGER.info("Binding exchange: %s", self.exchange)
        self.waiting_channel()
        if isinstance(self.channel, Channel):
            self.channel.exchange_bind(
                destination=self.exchange_bind_destination,
                source=self.exchange_bind_source,
                routing_key=self.exchange_bind_routing_key,
                arguments=self.exchange_bind_arguments,
                callback=self.on_exchange_bind_ok,
            )

    def on_exchange_bind_ok(self, method_frame: Method):
        """Invoked by pika when the Exchange.Bind method has completed. At this
        point we will set the prefetch count for the channel.

        :param pika.frame.Method method_frame: Method: The Exchange.BindOk response frame
        :param dict: Config

        """

        LOGGER.info("Exchange binded: %s", self.exchange)
        self._exchange_is_binded = True

    def run(self, blocking: bool = False):
        super().run(blocking)
        if blocking:
            self.waiting_exchange_is_binded()
