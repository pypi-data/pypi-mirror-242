#!/usr/bin/env python
# pylint: disable=C0114,C0116

from typing import Any, Dict
from delpinos.core.functions.dict_function import dicts_merge
from delpinos.api.core.config import config as core_config
from delpinos.rabbitmq.api.configs.rabbitmq_connection import (
    config as rabbitmq_connection,
)


config: Dict[str, Any] = dicts_merge(
    core_config,
    rabbitmq_connection,
)
