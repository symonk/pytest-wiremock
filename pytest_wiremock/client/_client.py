from __future__ import annotations

import typing
from contextlib import AbstractContextManager

import httpx

from ._constants import HTTP_DELETE
from ._constants import HTTP_GET
from ._constants import HTTP_POST
from ._decorators import success_when
from ._models_schemas import FixedDelay
from ._models_schemas import FixedDelaySchema
from ._models_schemas import WmSchema


class WiremockClient(AbstractContextManager):
    """
    A (synchronous) python client for the wiremock admin API.

    Things to consider:
        :: Reusable request -> response dispatching
        :: Reusable status code handling
        :: Session based

    # Todo: Check the host initially and gracefully error rather than raise ConnectError for conn ref.
    """

    def __init__(self, host: str = "localhost", port: int = 8080, timeout: float = 30.00) -> None:
        self.host = f"http://{host}:{port}/__admin/"
        self.client = httpx.Client(base_url=self.host, timeout=timeout)

    @success_when(200)
    def delete_all_stubs(self) -> httpx.Response:
        """Delete all registered stubs"""
        return self(method=HTTP_DELETE, url="/mappings")

    @success_when(200)
    def reset_all_stubs(self) -> httpx.Response:
        """Reset all registered stubs to what is defined on disk in the backing store."""
        return self(method=HTTP_POST, url="/mappings/reset")

    @success_when(200)
    def get_settings(self) -> httpx.Response:
        return self(method=HTTP_GET, url="/settings")

    @success_when(200)
    def set_fixed_delay(self, fixed_delay: int) -> httpx.Response:
        """
        Configure a global fixed delay for all registered stubs. The response will not be returned
        until after this delay.

        :param fixed_delay: Number of milliseconds to wait before issuing the response.
        """
        return self(method=HTTP_POST, url="/settings", payload=FixedDelay(fixed_delay), schema=FixedDelaySchema)

    @success_when(200)
    def reset(self) -> httpx.Response:
        """Reset mappings to the default state and reset the request journal"""
        return self(method=HTTP_POST, url="/reset")

    @success_when(200)
    def shutdown(self) -> httpx.Response:
        """Shutdown the wire mock instance"""
        return self(method=HTTP_POST, url="/shutdown")

    def __call__(
        self,
        *,
        method: str,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict] = None,
    ):
        """Dispatch a HTTP request"""
        if schema is not None:
            payload = schema(**schema_kw or {}).dump(payload)
        return self.client.request(method=method, url=url, json=payload)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def __del__(self) -> None:
        self.client.close()
