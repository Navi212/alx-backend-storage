#!/usr/bin/env python3
""" The `exercise` supplies a class `Cache` """
import redis
from typing import Union, Optional, Callable
import uuid


class Cache:
    """ Defines a `Cache` class """
    def __init__(self):
        """
        Constructor method called whenever an instance is created
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store:  Function that takes `data` arg and returns a str

        Args:
        data:   str | bytes | int | bytes

        Return:
        str
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable]) -> Union[str, bytes, int, float]:
        """
        get:    Function that takes arg `key` returns a converted value

        args:
        key:    str
        fn:     function/Callable

        Return: str | bytes | int | float
        """
        value = self._redis.get(key)
        if (fn and value):
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        get_str: Function taking arg `key` and converts
                 the value to str and returns it

        args:
        key:     str

        Return:  str | None
        """
        value = sef._redis.get(key)
        if value:
            return value.decode("utf-8")
        else:
            return None

    def get_int(self, key: str) -> int:
        """
        get_int: Function taking arg `key` and converts
                 the value to int and returns it

        args:
        key:     str

        Return:  int
        """
        value = self._redis.get(key)
        if value:
            return int(value.decode("utf-8"))
        return 0
