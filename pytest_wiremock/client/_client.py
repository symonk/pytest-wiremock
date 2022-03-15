from __future__ import annotations

import typing
from types import TracebackType

import httpx
from httpx import ConnectError
from httpx import TimeoutException as HttpxTimeoutException

from ._constants import HTTPVerbs
from ._decorators import handle_response
from ._exceptions import WiremockConnectionException
from ._exceptions import WiremockTimeoutException
from ._models_schemas import FixedDelay
from ._models_schemas import FixedDelaySchema
from ._models_schemas import WmSchema
from ._types import TimeoutTypes
from ._types import VerifyTypes


class Dispatcher:
    """
    Dispatch requests through the underlying client.
    """

    def __init__(self, client: httpx.Client, host: str) -> None:
        self.client = client
        self.host = host

    def post(self):
        ...

    def put(self):
        ...

    def delete(self):
        ...

    def get(self):
        ...

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
        except HttpxTimeoutException as exc:
            raise WiremockTimeoutException(None, str(exc)) from None
        except ConnectError:
            raise WiremockConnectionException(self.host) from None


class WiremockClient:
    """
    A (synchronous) python client for the wiremock admin API.
    The WiremockClient instance is a facade of various wiremock endpoints; to access the endpoints
    refer to:
        https://wiremock.org/docs/api/

        :param host: The host of the running wiremock instance
        :param port: The port wiremock is listening on
        :param timeout: Configuration for connect, read, write & pool timeouts.
        Timeout can be either a tuple of upto length 4; a single float (for all equal timeouts)
        or a httpx.Timeout instance.
        :param client_verify: configure ssl configurations; False by default and not checking SSL certs.
    """

    def __init__(
        self,
        https: bool = False,
        host: str = "localhost",
        port: int = 8080,
        timeout: TimeoutTypes = 30.00,
        client_verify: VerifyTypes = False,
        dispatcher: typing.Callable[[httpx.Client, str], Dispatcher] = Dispatcher,
    ) -> None:
        protocol = "http" if not https else "https"
        self.host = f"{protocol}://{host}:{port}/__admin/"
        self.client = httpx.Client(base_url=self.host, timeout=timeout, verify=client_verify)
        self.dispatcher = dispatcher(self.client, self.host)
        self.stubs = StubsEndpoint(self.dispatcher)
        self.requests = RequestsEndpoint(self.dispatcher)
        self.near_misses = NearMissesEndpoint(self.dispatcher)
        self.recordings = RecordingsEndpoint(self.dispatcher)
        self.scenarios = ScenariosEndpoint(self.dispatcher)
        self.settings = SystemEndpoint(self.dispatcher)

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


class SystemEndpoint:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def set_fixed_delay(self, fixed_delay: int) -> httpx.Response:
        """
        Configure a global fixed delay for all registered stubs. The response will not be returned
        until after this delay.

        :param fixed_delay: Number of milliseconds to wait before issuing the response.
        """
        return self.dispatcher(
            method=HTTPVerbs.POST, url="/settings", payload=FixedDelay(fixed_delay), schema=FixedDelaySchema
        )

    @handle_response(200)
    def reset(self) -> httpx.Response:
        """Reset mappings to the default state and reset the request journal"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/reset")

    @handle_response(200)
    def shutdown(self) -> httpx.Response:
        """Shutdown the wire mock instance"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/shutdown")


class StubsEndpoint:
    """
    Facade into mappings.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def delete_all_stubs(self) -> httpx.Response:
        """Delete all registered stubs"""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    @handle_response(200)
    def reset_all_stubs(self) -> httpx.Response:
        """Reset all registered stubs to what is defined on disk in the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/reset")

    @handle_response(200)
    def save_stubs(self) -> httpx.Response:
        """Save all persistent stubs to the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/save")

    @handle_response(200)
    def delete_stub_with_uuid(self, uuid: str) -> httpx.Response:
        """Delete the stub with a matching uuid."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url=f"/mappings/delete/{uuid}")


class RequestsEndpoint:
    """
    Facade into requests.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def get_requests(self, limit: int, since: str) -> httpx.Response:
        """Retrieve all requests within limit that have been recorded as of since."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/requests", params={"limit": limit, "since": since})

    @handle_response(200)
    def delete_requests(self) -> httpx.Response:
        """Delete all the requests."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/requests")


class NearMissesEndpoint:
    """
    Facade into near misses.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher


class RecordingsEndpoint:
    """
    Facade into recordings.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher


class ScenariosEndpoint:
    """
    Facade into scenarios.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def reset_scenarios(self) -> httpx.Response:
        """Reset the state of all scenarios."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/scenarios/reset")

    @handle_response(200)
    def get_settings(self) -> httpx.Response:
        return self.dispatcher(method=HTTPVerbs.GET, url="/settings")
