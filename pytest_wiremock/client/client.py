from __future__ import annotations

import typing

import httpx

from .decorators import success_when


class RequestDispatcher:
    def __init__(self, client: httpx.Client):
        self.client = client

    def __call__(self, method: str, url: str, payload: typing.Optional[typing.Any] = None) -> httpx.Response:
        return self.client.request(method, url, json=payload)


class WiremockClient:
    """
    A (synchronous) python client for the wiremock admin API.

    Things to consider:
        :: Reusable request -> response dispatching
        :: Reusable status code handling
        :: Session based

    # Todo: Check the host initially and gracefully error rather than raise ConnectError for conn ref.
    """

    def __init__(
        self, host: str, port: int, dispatcher: typing.Type[typing.Callable] = RequestDispatcher, timeout: float = 30.00
    ) -> None:
        self.host = f"http://{host}:{port}/__admin/"
        self.client = httpx.Client(base_url=self.host, timeout=timeout)
        self.dispatcher = dispatcher(self.client)

    @success_when(204)
    def reset(self) -> httpx.Response:
        return self.dispatcher(method="POST", url="/reset")

    @success_when(201)
    def shutdown(self) -> httpx.Response:
        return self.dispatcher(method="POST", url="/shutdown")

    def __enter__(self) -> WiremockClient:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
