#!/usr/bin/env python3
"""
The `exercise` module supplies a class `Cache`.

Task 0:
-------
Writing strings to Redis
Create a Cache class. In the __init__ method, store an instance of
the Redis client as a private variable named _redis (using redis.Redis())
and flush the instance using flushdb.

Create a store method that takes a data argument and returns a string.
The method should generate a random key (e.g. using uuid), store the
input data in Redis using the random key and return the key.

Type-annotate store correctly. Remember that data can be a str, bytes,
int or float.

Task 1:
-------
Reading from Redis and recovering original type
Redis only allows to store string, bytes and numbers (and lists thereof).
Whatever you store as single elements, it will be returned as a byte string.
Hence if you store "a" as a UTF-8 string, it will be returned as b"a" when
retrieved from the server.

In this exercise we will create a get method that take a key string argument
and an optional Callable argument named fn. This callable will be used to
convert the data back to the desired format.

Remember to conserve the original Redis.get behavior if the key does not exist.

Also, implement 2 new methods: get_str and get_int that will automatically
parametrize Cache.get with the correct conversion function.
The following code should not raise:

Task 2:
------
Incrementing values
Familiarize yourself with the INCR command and its python equivalent.

In this task, we will implement a system to count how many times methods
of the Cache class are called.

Above Cache define a count_calls decorator that takes a single method
Callable argument and returns a Callable.

As a key, use the qualified name of method using the __qualname__ dunder
method.

Create and return function that increments the count for that key every
time the method is called and returns the value returned by the original
method.

Remember that the first argument of the wrapped function will be self which
is the instance itself, which lets you access the Redis instance.

Protip: when defining a decorator it is useful to use functool.wraps to
conserve the original function’s name, docstring, etc. Make sure you use it
as described here.
Decorate Cache.store with count_calls.

Task 3:
------
Storing lists
Familiarize yourself with redis commands RPUSH, LPUSH, LRANGE, etc.
In this task, we will define a call_history decorator to store the
history of inputs and outputs for a particular function.

Everytime the original function will be called, we will add its input
parameters to one list in redis, and store its output into another list.

In call_history, use the decorated function’s qualified name and append
":inputs" and ":outputs" to create input and output list keys, respectively.

call_history has a single parameter named method that is a Callable and
returns a Callable.

In the new function that the decorator will return, use rpush to append
the input arguments. Remember that Redis can only store strings, bytes
and numbers. Therefore, we can simply use str(args) to normalize.
We can ignore potential kwargs for now.

Execute the wrapped function to retrieve the output. Store the output using
rpush in the "...:outputs" list, then return the output.
Decorate Cache.store with call_history.
"""
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
