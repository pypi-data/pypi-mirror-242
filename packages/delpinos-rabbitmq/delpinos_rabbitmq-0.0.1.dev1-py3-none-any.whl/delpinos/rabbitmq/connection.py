# -*- coding: utf-8 -*-
# pylint: disable=C0114,R0902,R0913,R0904,W0613

import time
import logging
import typing
import threading
from pika import SelectConnection
from pika.adapters import select_connection
from pika.connection import Parameters, URLParameters
from delpinos.core.factories.factory import Factory

DEFAULT_RABBITMQ_CONNECTION_RETRIES = 1000
DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT = 15

LOGGER = logging.getLogger(__name__)


class RabbitmqConnectionWrapper:
    _thread: threading.Thread | None
    _connection: SelectConnection | None
    _last_exeption: Exception
    _running: bool
    _closing: bool
    _attempt: int
    _parameters: Parameters | None
    _on_open_connection_ok_callback: typing.Callable[[], None] | None
    _on_open_connection_error_callback: typing.Callable[[Exception], None] | None
    _on_close_connection_callback: typing.Callable[[Exception], None] | None
    _ioloop = select_connection.IOLoop()
    _retries: int
    _timeout: int

    def __init__(
        self,
        parameters: Parameters | typing.Dict[str, typing.Any] | None = None,
        retries: int | None = None,
        timeout: int | None = None,
        on_open_callback: typing.Callable[[], None] | None = None,
        on_open_error_callback: typing.Callable[[Exception], None] | None = None,
        on_close_callback: typing.Callable[[Exception], None] | None = None,
    ):
        if not isinstance(parameters, (Parameters, dict)):
            parameters = {}
        if isinstance(parameters, dict):
            url = parameters.get("url") or "amqp://guest:guest@localhost:5672/%2F"
            parameters = URLParameters(url)
        self._thread = None
        self._connection = None
        self._last_exeption = Exception()
        self._running = False
        self._closing = False
        self._attempt = 0
        self._parameters = parameters
        self._on_open_connection_ok_callback = on_open_callback
        self._on_open_connection_error_callback = on_open_error_callback
        self._on_close_connection_callback = on_close_callback
        self._ioloop = select_connection.IOLoop()
        self._retries = int(
            retries
            if isinstance(retries, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES,
        )
        self._timeout = int(
            timeout
            if isinstance(timeout, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT,
        )

    @property
    def ioloop(self) -> select_connection.IOLoop:
        return self._ioloop

    @property
    def is_open(self) -> bool:
        return bool(self.connection and self.connection.is_open)

    @property
    def is_running(self) -> bool:
        return bool(self._running)

    @property
    def is_closing(self) -> bool:
        return bool(self._closing)

    @property
    def is_closed(self):
        if isinstance(self.connection, SelectConnection):
            return self.connection.is_closed
        return self.is_closing

    @property
    def thread(self) -> threading.Thread | None:
        return self._thread

    @property
    def connection(self) -> SelectConnection | None:
        return self._connection

    @property
    def parameters(self) -> Parameters | None:
        return self._parameters

    @property
    def timeout(self) -> int:
        return self._timeout

    @property
    def retries(self) -> int:
        return self._retries

    @property
    def attempt(self) -> int:
        return self._attempt

    def waiting_connection(self):
        is_running = False
        while not isinstance(self.connection, SelectConnection):
            if not is_running and not self.is_running:
                is_running = True
                self.run()
            continue
        return self

    def waiting_running(self):
        while not self.is_running:
            continue
        return self

    def waiting_connection_is_open(self):
        self.waiting_connection()
        while not self.is_open:
            continue
        return self

    def waiting_connection_is_closed(self):
        while not self.is_closed:
            continue
        return self

    def connect(self) -> SelectConnection:
        return SelectConnection(
            parameters=self._parameters,
            on_open_callback=self.on_open_callback,
            on_open_error_callback=self.on_open_error_callback,
            on_close_callback=self.on_close_callback,
            custom_ioloop=self.ioloop,
        )

    def reconnect(self):
        if self.attempt >= self.retries:
            self.stop(True)
            if callable(self._on_open_connection_error_callback):
                self._on_open_connection_error_callback(self._last_exeption)
            return

        if not self.is_closing:
            self._attempt += 1
            try:
                self._running = False
                if isinstance(self.connection, SelectConnection):
                    self.connection.close()
                    self.waiting_connection_is_closed()
                    LOGGER.warn("Connection Stopped")
                self.ioloop.stop()
                LOGGER.warn("Connection IOLoop Stopped")
                self._connection = None
            except Exception as err:
                LOGGER.error(err)
            time.sleep(self._timeout)
            self.run(blocking=False)

    def on_open_callback(self, connection: SelectConnection):
        LOGGER.warn("Connection opened")
        self._connection = connection
        self._attempt = 0
        if callable(self._on_open_connection_ok_callback):
            self._on_open_connection_ok_callback()

    def on_close_callback(self, connection, err: Exception):
        if self.is_closing:
            self.ioloop.stop()
            if callable(self._on_close_connection_callback):
                self._on_close_connection_callback(err)
        else:
            self.on_open_error_callback(connection, err)

    def on_open_error_callback(self, connection, err: Exception):
        LOGGER.warning(
            "Connection open failed, reopening in %s seconds: (%s)", self._timeout, err
        )
        self._last_exeption = err
        self._connection = connection
        self.reconnect()

    def on_connection_open_ok(self):
        pass

    def on_connection_open_error(self, err: Exception):
        raise err

    def on_connection_close(self, err: Exception):
        pass

    def start_ioloop(self):
        def start():
            try:
                self.ioloop.start()
            except RuntimeError:
                pass

        self._thread = threading.Thread(target=start, daemon=True)
        self._thread.start()

    def run(self, blocking: bool = False):
        if not self.is_running:
            self._running = True
            self._closing = False
            self._connection = self.connect()
            self._thread = threading.Thread(target=self.ioloop.start, daemon=True)
            self._thread.start()
        if blocking:
            self.waiting_connection_is_open()

    def stop(self, blocking: bool = False):
        self._closing = True
        if self.is_running:
            LOGGER.warn("Stopping Connection")
            self._running = False
            if isinstance(self.connection, SelectConnection):
                self.connection.close()
                if blocking:
                    self.waiting_connection_is_closed()
                LOGGER.warn("Connection Stopped")
            self.ioloop.stop()
            LOGGER.warn("Connection IOLoop Stopped")
            self._connection = None


class RabbitmqConnection(Factory):
    def setup(self):
        if isinstance(self.connection, RabbitmqConnectionWrapper):
            retries = self.connection.retries
            timeout = self.connection.timeout
            parameters = self.connection.parameters
        else:
            parameters = self.get("connection_parameters")
            retries = self.get("connection_retries")
            timeout = self.get("connection_timeout")
            self.set("connection", None)
        retries = int(
            retries
            if isinstance(retries, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES,
        )
        timeout = int(
            timeout
            if isinstance(timeout, int)
            else DEFAULT_RABBITMQ_CONNECTION_RETRIES_TIMEOUT,
        )
        if not isinstance(parameters, (Parameters, dict)):
            parameters = {}
        if isinstance(parameters, dict):
            url = parameters.get("url") or "amqp://guest:guest@localhost:5672/%2F"
            parameters = URLParameters(url)
        self.set("connection_retries", retries, int)
        self.set("connection_timeout", timeout, int)
        self.set("connection_parameters", parameters, Parameters)

    @property
    def connection(self) -> RabbitmqConnectionWrapper | None:
        connection = self.get("connection")
        if isinstance(connection, RabbitmqConnectionWrapper):
            if connection.is_closed:
                connection = None
            self.set("connection", connection)
        return connection

    @property
    def connection_timeout(self) -> int:
        return self.get("connection_timeout", int)

    @property
    def connection_retries(self) -> int:
        return self.get("connection_retries", int)

    @property
    def connection_attempt(self) -> int:
        return self.get("connection_attempt", int)

    @property
    def connection_parameters(self) -> Parameters:
        return self.get("connection_parameters", Parameters)

    @property
    def is_open_connection(self) -> bool:
        return (
            isinstance(self.connection, RabbitmqConnectionWrapper)
            and self.connection.is_open
        )

    @property
    def is_closed_connection(self):
        return (
            not isinstance(self.connection, RabbitmqConnectionWrapper)
            or self.connection.is_closed
        )

    @property
    def is_running_connection(self) -> bool:
        return (
            isinstance(self.connection, RabbitmqConnectionWrapper)
            and self.connection.is_running
        )

    @property
    def is_closing_connection(self) -> bool:
        return (
            not isinstance(self.connection, RabbitmqConnectionWrapper)
            or self.connection.is_closed
        )

    def waiting_connection(self):
        is_running = False
        while not isinstance(self.connection, RabbitmqConnectionWrapper):
            # if not is_running and not self.is_running_connection:
            #    is_running = True
            #    self.run(False)
            continue
        return self

    def waiting_running_connection(self):
        while not self.is_running_connection:
            continue
        return self

    def waiting_open_connection(self):
        self.waiting_connection()
        while not self.is_open_connection:
            continue
        return self

    def waiting_closed_connection(self):
        while not self.is_closed_connection:
            continue
        return self

    def on_open_connection_ok(self):
        pass

    def on_open_connection_error(self, err: Exception):
        raise err

    def on_close_connection(self, err: Exception):
        pass

    def build_connection(self) -> RabbitmqConnectionWrapper:
        return RabbitmqConnectionWrapper(
            parameters=self.connection_parameters,
            retries=self.connection_retries,
            timeout=self.connection_timeout,
            on_open_callback=self.on_open_connection_ok,
            on_open_error_callback=self.on_open_connection_error,
            on_close_callback=self.on_close_connection,
        )

    def run(self, blocking: bool = False):
        if not self.is_running_connection:
            if not isinstance(self.connection, RabbitmqConnectionWrapper):
                self.set(
                    "connection", self.build_connection(), RabbitmqConnectionWrapper
                )
            if isinstance(self.connection, RabbitmqConnectionWrapper):
                self.connection.run(blocking)
        if blocking:
            self.waiting_open_connection()

    def stop(self, blocking: bool = False):
        if self.is_running_connection and isinstance(
            self.connection, RabbitmqConnectionWrapper
        ):
            self.connection.stop(blocking)
        if blocking:
            self.waiting_closed_connection()

    def health_check(self) -> tuple:
        try:
            if not self.is_running_connection:
                raise Exception("Rabbitmq connection is not running")
            if self.is_closed_connection:
                raise Exception("Rabbitmq connection is closed")
            if not self.is_open_connection:
                raise Exception("Rabbitmq connection is not open")
            return True, "Success"
        except Exception as err:
            return False, str(err)
