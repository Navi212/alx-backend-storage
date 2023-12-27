#!/usr/bin/env python3
"""
The `web.py` module supplies a decorator function `wrapper` and `get_page`
function.
"""
import redis
import requests
from functools import wraps
from typing import Callable


def count_visits(method: Callable) -> Callable:
    """
    count_visits: Function that takes a function as an argument
                  and returns a function

    Args:
    method:       function/Callable

    Return:
    function/Callable
    """
    r = redis.Redis()

    @wraps(method)
    def wrapper(*args, **kwargs) -> str:
        """
        wrapper:    represents the function/callable passed
                    as argument to the `count_visits` function

        Args:
        url

        Return
        str
        """
        url = str(args[0])
        key = f"count:{url}"
        r.incr(key)
        cached_url = r.get(url)
        # If url was actually cached, the return the
        # decoded version to the client
        if cached_url:
            return cached_url.decode("utf-8")
        # Else not cached, then call the original function
        # here `get_page` implementing `get_page` logic
        # and the return a str into `html_content`
        html_content = method(*args, **kwargs)
        # Then `Cache it` by setting the url as a `key` with
        # 10secs expiration time with a value of `html_content returned
        r.setex(url, 10, html_content)
        # Then return the `str` based on the original's function
        # `get_page` code logic
        return html_content
    # Finally return the `wrapper` making the decoration possible
    return wrapper


@count_visits
def get_page(url: str) -> str:
    """
    get_page:   Function that takes a `url` argument
                and returns the html content of the url

    Args:
    url:        str

    Return:
    str
    """
    return requests.get(url).text


# Test script here
if __name__ == "__main__":
    r = redis.Redis()
    test_url = "http://slowwly.robertomurray.co.uk"
    test_content = get_page(test_url)
    print(test_content)
    print(f"Visits for {test_url}:-> {r.get(f'count:{test_url}').decode()}")
