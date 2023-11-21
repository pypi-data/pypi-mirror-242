# -*- coding: utf-8 -*-
# pylint: disable=C0114

import os
from typing import Any, Dict
from urllib.parse import quote_plus

DEFAULT_DATABASE_DRIVER = "postgresql+psycopg2"
DEFAULT_DATABASE_USER = "postgres"
DEFAULT_DATABASE_PASSWORD = "postgres"
DEFAULT_DATABASE_HOST = "localhost"
DEFAULT_DATABASE_PORT = "5432"
DEFAULT_DATABASE_NAME = "postgres"
DEFAULT_DATABASE_ARGS = ""


def build_database_connection_uri() -> str:
    uri = os.getenv("DATABASE_URI", os.getenv("DATABASE_URL"))
    if not uri:
        driver = os.getenv("DATABASE_DRIVER", DEFAULT_DATABASE_DRIVER)
        user = os.getenv("DATABASE_USER", DEFAULT_DATABASE_USER)
        password = os.getenv("DATABASE_PASSWORD", DEFAULT_DATABASE_PASSWORD)
        host = os.getenv("DATABASE_HOST", DEFAULT_DATABASE_HOST)
        port = os.getenv("DATABASE_PORT", DEFAULT_DATABASE_PORT)
        name = os.getenv("DATABASE_NAME", DEFAULT_DATABASE_NAME)
        args = os.getenv("DATABASE_ARGS", DEFAULT_DATABASE_ARGS)
        uri_parts = [
            driver,
            "://",
            user,
            ":",
            quote_plus(password),
            "@",
            host,
            ":",
            port,
            "/",
            quote_plus(name),
            "?",
            args,
        ]
        uri = ("".join(uri_parts)).replace("??", "?").strip("?").strip("/")
    return uri


config: Dict[str, Any] = {
    "sqlalchemy": {
        "connection": {
            "uri": build_database_connection_uri(),
        },
    },
}
