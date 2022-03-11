from __future__ import annotations

import typing
from types import TracebackType

import httpx
from httpx import ConnectError

from ._constants import HTTP_DELETE
from ._constants import HTTP_GET
from ._constants import HTTP_POST
from ._decorators import success_when
from ._exceptions import WiremockConnectionError
from ._models_schemas import FixedDelay
from ._models_schemas import FixedDelaySchema
from ._models_schemas import WmSchema


class WiremockClient:
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

    # --- Stub Code --- #
    @success_when(200)
    def delete_all_stubs(self) -> httpx.Response:
        """Delete all registered stubs"""
        return self(method=HTTP_DELETE, url="/mappings")

    @success_when(200)
    def reset_all_stubs(self) -> httpx.Response:
        """Reset all registered stubs to what is defined on disk in the backing store."""
        return self(method=HTTP_POST, url="/mappings/reset")

    @success_when(200)
    def save_stubs(self) -> httpx.Response:
        """Save all persistent stubs to the backing store."""
        return self(method=HTTP_POST, url="/mappings/save")

    @success_when(200)
    def delete_stub_with_uuid(self, uuid: str) -> httpx.Response:
        """Delete the stub with a matching uuid."""
        return self(method=HTTP_DELETE, url=f"/mappings/delete/{uuid}")

    # --- Request Code --- #

    @success_when(200)
    def get_requests(self, limit: int, since: str) -> httpx.Response:
        """Retrieve all requests within limit that have been recorded as of since."""
        return self(method=HTTP_GET, url="/requests", params={"limit": limit, "since": since})

    @success_when(200)
    def delete_requests(self) -> httpx.Response:
        """Delete all the requests."""
        return self(method=HTTP_DELETE, url="/requests")

    # --- Scenario Code --- #
    @success_when(200)
    def reset_scenarios(self) -> httpx.Response:
        """Reset the state of all scenarios."""
        return self(method=HTTP_POST, url="/scenarios/reset")

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
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ):
        """Dispatch a HTTP request"""
        if schema is not None:
            payload = schema(**schema_kw or {}).dump(payload)
        try:
            return self.client.request(method=method, url=url, json=payload)
        except ConnectError:
            raise WiremockConnectionError(self.host) from None

    def __enter__(self) -> WiremockClient:
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]] = None,
        exc_val: typing.Optional[BaseException] = None,
        exc_tb: typing.Optional[TracebackType] = None,
    ):
        self.client.close()

    def __del__(self) -> None:
        self.client.close()
