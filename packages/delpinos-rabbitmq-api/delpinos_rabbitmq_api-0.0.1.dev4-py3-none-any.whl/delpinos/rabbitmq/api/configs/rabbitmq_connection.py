# -*- coding: utf-8 -*-
# pylint: disable=C0114

import os
from urllib.parse import quote_plus
from typing import Any, Dict

DEFAULT_RABBITMQ_CONNECTION_USER = "guest"
DEFAULT_RABBITMQ_CONNECTION_PASSWORD = "guest"
DEFAULT_RABBITMQ_CONNECTION_HOST = "localhost"
DEFAULT_RABBITMQ_CONNECTION_PORT = "5672"
DEFAULT_RABBITMQ_CONNECTION_VHOST = "/"
DEFAULT_RABBITMQ_CONNECTION_ARGS = ""


def build_rabbitmq_connection_uri():
    uri = os.getenv("RABBITMQ_CONNECTION_URI", os.getenv("RABBITMQ_CONNECTION_URL"))
    if not uri:
        user = os.getenv("RABBITMQ_CONNECTION_USER", DEFAULT_RABBITMQ_CONNECTION_USER)
        password = os.getenv(
            "RABBITMQ_CONNECTION_PASSWORD", DEFAULT_RABBITMQ_CONNECTION_PASSWORD
        )
        host = os.getenv("RABBITMQ_CONNECTION_HOST", DEFAULT_RABBITMQ_CONNECTION_HOST)
        port = os.getenv("RABBITMQ_CONNECTION_PORT", DEFAULT_RABBITMQ_CONNECTION_PORT)
        vhost = os.getenv(
            "RABBITMQ_CONNECTION_VHOST", DEFAULT_RABBITMQ_CONNECTION_VHOST
        )
        args = os.getenv("RABBITMQ_CONNECTION_ARGS", DEFAULT_RABBITMQ_CONNECTION_ARGS)
        uri_parts = [
            "amqp://",
            user,
            ":",
            quote_plus(password),
            "@",
            host,
            ":",
            port,
            "/",
            quote_plus(vhost),
            "?",
            args,
        ]
        uri = ("".join(uri_parts)).replace("??", "?").strip("?").strip("/")
    return uri


config: Dict[str, Any] = {
    "rabbitmq": {
        "connection_parameters": {
            "url": build_rabbitmq_connection_uri(),
        },
    },
}
