from __future__ import annotations

import typing
from types import TracebackType

import httpx

from ._exceptions import WiremockConnectionException
from ._exceptions import WiremockForbiddenException
from ._exceptions import WiremockMalformedRequest
from ._exceptions import WiremockNotFoundException
from ._exceptions import WiremockServerException
from ._exceptions import WiremockTimeoutException
from ._types import TimeoutTypes
from ._types import VerifyTypes
from .endpoints import NearMissesEndpoint
from .endpoints import RecordingsEndpoint
from .endpoints import RequestsEndpoint
from .endpoints import ScenariosEndpoint
from .endpoints import StubsEndpoint
from .endpoints import SystemEndpoint
from .resources import WmSchema


class WiremockClient:
    """
    A (synchronous) python client for the wiremock admin API.
    The WiremockClient instance is a facade of various wiremock endpoints; to access the endpoints
    refer to:
        https://wiremock.org/docs/api/

        :param host: The host of the running wiremock instance
        :param port: The port wiremock is listening on
        :param timeout: Configuration for connect, read, write & pool timeouts.
        Timeout can be either a tuple of up to length 4; a single float (for all equal timeouts)
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
    ) -> None:
        protocol = "http" if not https else "https"
        self.host = f"{protocol}://{host}:{port}/__admin/"
        self.client = httpx.Client(base_url=self.host, timeout=timeout, verify=client_verify)
        self.dispatcher = Dispatcher(self.client, self.host)
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


class Dispatcher:
    def __init__(self, client: httpx.Client, host: str) -> None:
        self.client = client
        self.host = host

    def __call__(
        self,
        *,
        method: str,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ) -> httpx.Response:
        """Dispatches HTTP requests.  We could implement this via __call__ but it should be private."""
        if schema is not None:
            payload = schema(**schema_kw or {}).dump(payload)
        try:
            response = self.client.request(method=method, url=url, json=payload)
            status = response.status_code
            if status in (200, 201):
                # Successfully fetching/creating a resource.
                return response
            elif status == 401:
                raise WiremockForbiddenException(response.text, status)
            elif status == 404:
                raise WiremockNotFoundException(
                    f"No wiremock instance running, {response.request.url} not found.", status
                )
            elif status == 422:
                raise WiremockMalformedRequest(response.text, status)
            elif status == 500:
                raise WiremockServerException(response.extensions["reason_phrase"], status)
        except httpx.TimeoutException as exc:
            raise WiremockTimeoutException(str(exc)) from None
        except httpx.ConnectError:
            raise WiremockConnectionException(self.host) from None
