#!/usr/bin/env python3
""" The `exercise` supplies a class `Cache` """
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    count_calls:    Function that takes a function as arg
                    and returns a function.
                    Counts number of times a function is called

    args:
    Callable:       A function

    Return:
    Callable:       A function
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Defines a `Cache` class """
    def __init__(self):
        """
        Constructor method called whenever an instance is created
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    # Cause count_calls methodto watch over how many times store
    # method is called
    @count_calls
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
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        get:    Function that takes arg `key` returns a converted value

        args:
        key:    str
        fn:     function/Callable

        Return: str | bytes | int | float
        """
        value = self._redis.get(key)
        # If a function is provided as a parameter
        if fn:
            return fn(value)
        # If no function is provided, return raw data
        # as per Redis default behaviour
        return value

    def get_str(self, key: str) -> str:
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
