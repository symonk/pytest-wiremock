from __future__ import annotations

import typing
from contextlib import AbstractContextManager

import httpx

from ._constants import HTTP_POST
from ._decorators import success_when
from ._models import LogNormalSettingsModel
from ._schemas import LogNormalSettingsSchema
from ._schemas import WmSchema

_SETTINGS_ALIAS = typing.Union[LogNormalSettingsModel]


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
    def update_settings(self, model: _SETTINGS_ALIAS) -> httpx.Response:
        """Update global settings"""
        return self(
            method=HTTP_POST,
            url="/settings",
            schema=LogNormalSettingsSchema,
            schema_kw={"only": ["fixed_delay"]},
            payload=model,
        )

    @success_when(200)
    def set_global_fixed_delay(self, delay: int) -> httpx.Response:
        """
        Set a global fixed delay across all stubs.  To provider this on a per stub basis
        configure the stub when creating one instead.
        """
        return self(method=HTTP_POST, url="/settings", payload={"fixedDelay": delay})

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
