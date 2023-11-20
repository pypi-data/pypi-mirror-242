# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613,R0801

import logging
import json
from typing import Any, Dict
from pika.spec import BasicProperties
from delpinos.core.factories.factory import Factory
from delpinos.rabbitmq.channel import RabbitmqChannel


LOGGER = logging.getLogger(__name__)


class RabbitmqProducer(RabbitmqChannel):
    @property
    def producer_exchange(self) -> str:
        return self.get("producer_exchange", str)

    @property
    def producer_routing_key(self) -> str:
        return self.get("producer_routing_key", str)

    @property
    def producer_mandatory(self) -> bool:
        return bool(self.get("producer_mandatory"))

    @property
    def producer_properties(self) -> BasicProperties | Dict[str, Any] | None:
        return self.get("producer_properties")

    def publish(
        self,
        body: str | Dict[str, Any] | bytes,
        exchange: str | None = None,
        routing_key: str | None = None,
        properties: BasicProperties | Dict[str, Any] | None = None,
        mandatory: bool | None = None,
    ):
        exchange = exchange if exchange else self.producer_exchange
        routing_key = routing_key if routing_key else self.producer_routing_key
        properties = (
            BasicProperties(**properties)
            if isinstance(properties, dict)
            else properties
            if isinstance(properties, BasicProperties)
            else self.producer_properties
        )
        properties = (
            BasicProperties(**properties)
            if isinstance(properties, dict)
            else properties
        )
        mandatory = bool(
            mandatory if mandatory is not None else self.producer_mandatory
        )
        if isinstance(body, bytes):
            new_body = body
        elif isinstance(body, dict):
            new_body = json.dumps(body, default=str).encode("utf-8")
        else:
            new_body = str(body).encode("utf-8")
        return self.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=new_body,
            properties=properties,
            mandatory=mandatory,
        )


class RabbitmqProducerFactory(Factory):
    def add_factories(self):
        super().add_factories()

        self.add_factory("rabbitmq.producer", self.factory_producer())

    def factory_producer(self):
        producer_config: dict = self.get("rabbitmq.producer_config", dict)

        def build(_):
            producer = RabbitmqProducer(**producer_config)
            producer.run(True)
            return producer

        return build

    @property
    def producer(self) -> RabbitmqProducer:
        return self.instance("rabbitmq.producer", RabbitmqProducer)
