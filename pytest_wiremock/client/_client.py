from __future__ import annotations

import typing
from contextlib import AbstractContextManager

import httpx

from ._constants import HTTP_POST
from ._decorators import success_when


class WiremockClient(AbstractContextManager):
    """
    A (synchronous) python client for the wiremock admin API.

    Things to consider:
        :: Reusable request -> response dispatching
        :: Reusable status code handling
        :: Session based

    # Todo: Check the host initially and gracefully error rather than raise ConnectError for conn ref.
    """

    def __init__(self, host: str, port: int, timeout: float = 30.00) -> None:
        self.host = f"http://{host}:{port}/__admin/"
        self.client = httpx.Client(base_url=self.host, timeout=timeout)

    @success_when(200)
    def reset(self) -> httpx.Response:
        return self(method=HTTP_POST, url="/reset")

    @success_when(200)
    def shutdown(self) -> httpx.Response:
        return self(method=HTTP_POST, url="/shutdown")

    def close_client(self) -> None:
        self.client.close()

    def __call__(self, method: str, url: str, payload: typing.Optional[typing.Any] = None):
        return self.client.request(method=method, url=url, json=payload)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_client()

    def __del__(self) -> None:
        self.close_client()
