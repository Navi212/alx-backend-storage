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
        url = args[0]
        key = f"count:{url}"
        r.incr(key)
        cached_html = r.get(url)
        if cached_html:
            return cached_html.decode("utf-8")
        html_content = method(*args, **kwargs)
        r.setex(url, 10, html_content)
        return html_content
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
    print(f"Visits count for {test_url}:{r.get(f'count:{test_url}').decode()}")
