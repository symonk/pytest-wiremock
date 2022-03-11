import functools

import httpx


def handle_response(expecting: int):
    """A simple decorator for enforcing expected response codes"""

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            response: httpx.Response = fn(*args, **kwargs)
            rcode = response.status_code
            if rcode != expecting:
                raise ValueError(f"Unexpected status code for {fn.__name__}, expected: {expecting} | got: {rcode}")
            return response

        return wrapper

    return deco
