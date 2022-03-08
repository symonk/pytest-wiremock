import functools

import httpx


def success_when(code: int):
    """A simple decorator for enforcing expected response codes"""

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            response: httpx.Response = fn(*args, **kwargs)
            if response.status_code != code:
                raise ValueError(f"Unexpected status code for {fn.__name__}, got: {code}")
            return response

        return wrapper

    return deco
