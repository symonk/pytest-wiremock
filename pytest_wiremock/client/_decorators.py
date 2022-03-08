import functools
import typing

import httpx

from ._schemas import WmSchema


def serialised_by(schema: typing.Type[WmSchema], schema_kwargs: typing.Optional[typing.Dict] = None):
    """Serialise the user provided model by the schema provided."""

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            kwargs["payload"] = schema(**schema_kwargs or {}).dump(kwargs["model"])
            return wrapper(*args, **kwargs)

        return wrapper

    return deco


def success_when(code: int):
    """A simple decorator for enforcing expected response codes"""

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            response: httpx.Response = fn(*args, **kwargs)
            rcode = response.status_code
            if rcode != code:
                raise ValueError(f"Unexpected status code for {fn.__name__}, expected: {code} | got: {rcode}")
            return response

        return wrapper

    return deco
