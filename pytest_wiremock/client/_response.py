import typing

import httpx


class WiremockResponse:
    """
    The response object for all calls to wiremock.
    """

    def __init__(self, delegate: httpx.Response) -> None:
        self.delegate = delegate
        self.status_code = delegate.status_code

    def json(self, **kwargs: typing.Any) -> typing.Any:
        return self.delegate.json(**kwargs)

    def __getattr__(self, item: str):
        """Dynamic dispatch to the underlying response."""
        attr = getattr(self.delegate, item)
        if callable(item):

            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)

            return wrapper
        return attr

    def __str__(self) -> str:
        return str(self.delegate)

    def __repr__(self) -> str:
        return repr(self.delegate)
