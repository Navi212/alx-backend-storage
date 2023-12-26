#!/usr/bin/env python3
""" The `exercise` supplies a class `Cache` """
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def replay(fn: Callable) -> None:
    """
    replay:    Function that takes a function/Callable as arg

    Args:
    fn:        function/Callable

    Return:
    None
    """
    r = redis.Redis()
    # Assigns method name via __qualname__ to `method_name`
    method_name = fn.__qualname__
    # Assigns number the function fn was called to `called_times`
    called_times = int(r.get(fn.__qualname__))
    print(f"{method_name} was called {called_times} times:")
    # Stores the inputs to `inputs` using the list key of
    # {}:inputs".format(method_name)
    inputs = r.lrange("{}:inputs".format(method_name), 0, -1)
    # Stores the ouputs to `outputs` using the list key of
    # {}:outputs".format(method_name)
    outputs = r.lrange("{}:outputs".format(method_name), 0, -1)
    # Zips inputs and outputs and prints out a fine print
    for inp, outp in zip(inputs, outputs):
        inp = inp.decode("utf-8")
        outp = outp.decode("utf-8")
        print(f"{method_name}(*{inp}) -> {outp}")


def call_history(method: Callable) -> Callable:
    """
    call_history: Function that takes a function as
                  argument and returns a function

    Args:
    function/callable

    Return:
    function/callable
    """
    method_name = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        A wrapper function that wraps around
        the orginal function `method` thereby
        adding more functionality and preserving
        the original functionality of `method`
        """
        inputs = str(args)
        self._redis.rpush(method_name + ":inputs", inputs)
        ret_val = method(self, *args, **kwargs)
        outputs = str(ret_val)
        self._redis.rpush(method_name + ":outputs", outputs)
        return outputs
    return wrapper


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
    @call_history
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

        Return:  str
        """
        value = sef._redis.get(key)
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
