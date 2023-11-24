import inspect
import itertools
import json
import os
from datetime import datetime
from enum import Enum, auto
from functools import wraps
from hashlib import sha256
from threading import Thread
from typing import Any, Callable, List, Union
from uuid import uuid4

from flask.app import Flask
from flask.config import Config
from pika import BlockingConnection, URLParameters, spec
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from retry import retry
from retry.api import retry_call

from rabbitmq_flask.ExchangeType import ExchangeType
from rabbitmq_flask.ExchangeParams import ExchangeParams
from rabbitmq_flask.QueueParams import QueueParams
from rabbitmq_flask.RabbitConsumerMiddleware import (
    RabbitConsumerMessage,
    RabbitConsumerMiddleware,
    call_middlewares,
)

# (queue_name, dlq_name, method, props, body, exception)
MessageErrorCallback = Callable[
    [str, Union[str, None], spec.Basic.Deliver, spec.BasicProperties, str, Exception], Any
]


class OptionalProps(Enum):
    """Props that can be optionally passed to functions decorated by @queue."""

    message_id = auto()
    sent_at = auto()
    message_version = auto()


class RabbitMQ:
    """Main class containing queue and message sending methods"""

    app: Flask
    config: Config

    connection_url: str
    get_connection: Callable[[], BlockingConnection]
    consumers: set

    exchange_name: str
    exchange_params: ExchangeParams

    queue_name: str
    queue_params: QueueParams

    on_message_error_callback: Union[MessageErrorCallback, None]
    middlewares: List[RabbitConsumerMiddleware]

    def __init__(
        self,
        app: Flask = None,
        connection_url: str = '',
        queue_params: QueueParams = QueueParams(),
        exchange_params: ExchangeParams = ExchangeParams(),
        middlewares: Union[List[RabbitConsumerMiddleware], None] = None
    ) -> None:
        self.app = None
        self.consumers = set()
        self.connection_url = connection_url
        self.exchange_params = exchange_params
        self.queue_params = queue_params
        self.middlewares = middlewares or []

        if app is not None:
            self.init_app(app, connection_url)

    # Inits class from flask app
    def init_app(
        self,
        app: Flask,
        connection_url: str,
        queue_params: QueueParams = QueueParams(),
        exchange_params: ExchangeParams = ExchangeParams(),
        on_message_error_callback: Union[MessageErrorCallback, None] = None,
        middlewares: Union[List[RabbitConsumerMiddleware], None] = None,
    ):
        """This callback can be used to initialize an application for the use with this RabbitMQ setup.

        Args:
            app (Flask): Flask app
            connection_url (str): RabbitMQ connection url
            queue_params (QueueParams): RabbitMQ Queue parameters
            exchange_params (ExchangeParams): RabbitMQ Exchange parameters
        """

        self.app = app
        self.config = app.config
        self.connection_url = connection_url
        self.queue_params = queue_params
        self.exchange_params = exchange_params
        self.exchange_name = 'default'
        self.middlewares.extend(middlewares or [])
        self.on_message_error_callback = on_message_error_callback
        self.get_connection = lambda: BlockingConnection(URLParameters(self.connection_url))
        self._validate_connection()

        # Run every consumer queue
        for consumer in self.consumers:
            consumer()

    def _validate_connection(self):
        try:
            connection = self.get_connection()
            if connection.is_open:
                self.app.logger.info("Connected to RabbitMQ")
                connection.close()
        except Exception as error:  # pylint: disable=broad-except
            self.app.logger.error("Invalid RabbitMQ connection")
            self.app.logger.error(error.__class__.__name__)

    def _build_queue_name(self, func: Callable):
        """Builds queue name from function name"""
        spacer = self.config["MQ_DELIMITER"] if "MQ_DELIMITER" in self.config else "." if self.queue_prefix else ""
        return self.queue_prefix + spacer + func.__name__.replace("_", spacer)

    def queue(
        self,
        routing_key: Union[str, List[str]],
        exchange_type: ExchangeType = ExchangeType.DEFAULT,
        queue: str = '',
        auto_ack: bool = False
    ):
        """Creates new RabbitMQ queue

        Args:
            queue (str): The queue name for this queue
            routing_key (str | list[str]): The routing key(s) for this queue
            exchange_type (ExchangeType, optional): The exchange type to be used. Defaults to TOPIC.
            auto_ack (bool, optional): If messages should be auto acknowledged. Defaults to False
        """

        def decorator(f):
            @wraps(f)
            def new_consumer():
                return self._setup_connection(
                    f,
                    queue,
                    routing_key,
                    exchange_type,
                    auto_ack
                )

            # adds consumer to consumers list if not initiated, or runs new consumer if already initiated
            if self.app is not None:
                new_consumer()
            else:
                self.consumers.add(new_consumer)
            return f
        return decorator

    def _setup_connection(
        self,
        func: Callable,
        queue: str,
        routing_key: Union[str, List[str]],
        exchange_type: ExchangeType,
        auto_ack: bool
    ):
        """Setup new queue connection in a new thread

        Args:
            func (Callable): function to run as callback for a new message
            routing_key (str | list[str]): routing key(s) for the new queue bind
            exchange_type (ExchangeType): Exchange type to be used with new queue
            auto_ack (bool): If messages should be auto acknowledged.
            dead_letter_exchange (bool): If a dead letter exchange should be created for this queue
            props_needed (list[str]): List of properties to be passed along with body
        """

        def create_queue():
            return self._add_exchange_queue(
                func,
                queue,
                routing_key,
                exchange_type,
                auto_ack
            )

        thread = Thread(target=create_queue, name=queue)
        thread.daemon = True
        thread.start()

    @retry((AMQPConnectionError, AssertionError), delay=5, jitter=(5, 15))
    def _add_exchange_queue(
        self,
        func: Callable,
        queue: str,
        routing_key: Union[str, List[str]],
        exchange_type: ExchangeType,
        auto_ack: bool
    ):
        """Creates or connects to new queue, retries connection on failure

        Args:
            func (Callable): function to run as callback for a new message
            routing_key (str | list[str]): routing key(s) for the new queue bind
            exchange_type (ExchangeType): Exchange type to be used with new queue
            auto_ack (bool): If messages should be auto acknowledged.
            dead_letter_exchange (bool): If a dead letter exchange should be created for this queue
            props_needed (list[str]): List of properties to be passed along with body
        """

        # Create connection channel
        connection = self.get_connection()
        channel = connection.channel()

        # Declare exchange
        channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=exchange_type,
            passive=self.exchange_params.passive,
            durable=self.exchange_params.durable,
            auto_delete=self.exchange_params.auto_delete,
            internal=self.exchange_params.internal,
        )

        channel.queue_declare(
            queue=queue,
            passive=self.queue_params.passive,
            durable=self.queue_params.durable,
            auto_delete=self.queue_params.auto_delete,
            exclusive=self.queue_params.exclusive
        )
        self.app.logger.info(f"Declaring Queue: {queue}")

        # Bind queue to exchange
        routing_keys = routing_key if isinstance(routing_key, list) else [routing_key]
        for routing_key in routing_keys:
            channel.queue_bind(
                exchange=self.exchange_name, queue=queue, routing_key=routing_key
            )

        def user_consumer(message: RabbitConsumerMessage, call_next) -> None:
            """User consumer as a middleware. Calls the consumer `func`."""
            func(
                routing_key=message.routing_key,
                body=message.parsed_body
            )
            call_next(message)

        def callback(
            _: BlockingChannel,
            method: spec.Basic.Deliver,
            props: spec.BasicProperties,
            body: bytes,
        ):
            with self.app.app_context():
                decoded_body = body.decode()

                try:
                    # Fetches original message routing_key from headers if it has been dead-lettered
                    routing_key = method.routing_key

                    if getattr(props, "headers", None) and props.headers.get("x-death"):
                        x_death_props = props.headers.get("x-death")[0]
                        routing_key = x_death_props.get("routing-keys")[0]

                    message = RabbitConsumerMessage(
                        routing_key, body, decoded_body, method, props
                    )
                    call_middlewares(
                        message, itertools.chain(list(self.middlewares), [user_consumer])
                    )

                    if not auto_ack:
                        # ack message after fn was ran
                        channel.basic_ack(method.delivery_tag)
                except Exception as err:  # pylint: disable=broad-except
                    self.app.logger.error(f"ERROR IN {queue}: {err}")
                    self.app.logger.exception(err)

                    try:
                        if not auto_ack:
                            channel.basic_reject(
                                method.delivery_tag, requeue=(not method.redelivered)
                            )
                    finally:
                        if self.on_message_error_callback is not None:
                            self.on_message_error_callback(
                                method, props, decoded_body, err
                            )

        channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=auto_ack
        )

        try:
            channel.start_consuming()
        except Exception as err:
            self.app.logger.error(err)
            channel.stop_consuming()
            connection.close()

            raise AMQPConnectionError from err

    def _send_msg(
        self, body, routing_key, exchange_type, message_version: str = "v1.0.0", **properties
    ):
        try:
            channel = self.get_connection().channel()

            channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type=exchange_type,
                passive=self.exchange_params.passive,
                durable=self.exchange_params.durable,
                auto_delete=self.exchange_params.auto_delete,
                internal=self.exchange_params.internal,
            )

            if self.msg_parser:
                body = self.msg_parser(body)

            if "message_id" not in properties:
                properties["message_id"] = sha256(json.dumps(body).encode("utf-8")).hexdigest()
            if "timestamp" not in properties:
                properties["timestamp"] = int(datetime.now().timestamp())

            if "headers" not in properties:
                properties["headers"] = {}
            properties["headers"]["x-message-version"] = message_version

            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=body,
                properties=spec.BasicProperties(**properties),
            )

            channel.close()
        except Exception as err:
            self.app.logger.error("Error while sending message")
            self.app.logger.error(err)

            raise AMQPConnectionError from err

    def send(
        self,
        body,
        routing_key: str,
        exchange_type: ExchangeType = ExchangeType.DEFAULT,
        retries: int = 5,
        message_version: str = "v1.0.0",
        **properties
    ):
        """Sends a message to a given routing key

        Args:
            body (str): The body to be sent
            routing_key (str): The routing key for the message
            exchange_type (ExchangeType, optional): The exchange type to be used. Defaults to ExchangeType.DEFAULT.
            retries (int, optional): Number of retries to send the message. Defaults to 5.
            message_version (str): Message version number.
            properties (dict[str, Any]): Additional properties to pass to spec.BasicProperties
        """

        thread = Thread(
            target=lambda: self.sync_send(
                body, routing_key, exchange_type, retries, message_version, **properties
            ),
        )
        thread.daemon = True
        thread.start()

    def sync_send(
        self,
        body,
        routing_key: str,
        exchange_type: ExchangeType = ExchangeType.DEFAULT,
        retries: int = 5,
        message_version: str = "v1.0.0",
        **properties
    ):
        """Sends a message to a given routing key synchronously

        Args:
            body (str): The body to be sent
            routing_key (str): The routing key for the message
            exchange_type (ExchangeType, optional): The exchange type to be used. Defaults to ExchangeType.DEFAULT.
            retries (int, optional): Number of retries to send the message. Defaults to 5.
            message_version (str): Message version number.
            properties (dict[str, Any]): Additional properties to pass to spec.BasicProperties
        """

        retry_call(
            self._send_msg,
            (body, routing_key, exchange_type, message_version),
            properties,
            exceptions=(AMQPConnectionError, AssertionError),
            tries=retries,
            delay=5,
            jitter=(5, 15)
        )
