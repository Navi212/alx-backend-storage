#!/usr/bin/env python3
""" The `exercise` supplies a class `Cache` """
import redis
import random
import uuid
from typing import Union


class Cache:
    """
    Defines a class `Cache`
    """
    def __init__(self):
        """
        init: Object constructor method
        """
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(data: Union[str, bytes, int, float]) -> str:
        """
        store: Function that takes data arg and returns a str

        Args:
        data:  str | bytes | int | float

        Return:
        str
        """
        key = str(uuid.uuid4()) + str(random.randint(1, 1000))
        self._redis.set(key, data)
        return key
