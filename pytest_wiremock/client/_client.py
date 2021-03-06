from __future__ import annotations

import typing
from types import TracebackType

import httpx

from ._endpoints_mappings import MappingsEndpoint
from ._endpoints_near_misses import NearMissesEndpoint
from ._endpoints_recordings import RecordingsEndpoint
from ._endpoints_requests import RequestsEndpoint
from ._endpoints_scenarios import ScenariosEndpoint
from ._endpoints_system import SystemEndpoint
from ._exceptions import WiremockConnectionException
from ._exceptions import WiremockForbiddenException
from ._exceptions import WiremockMalformedRequest
from ._exceptions import WiremockNotFoundException
from ._exceptions import WiremockServerException
from ._exceptions import WiremockTimeoutException
from ._response import WiremockResponse
from ._schemas import WiremockSchema
from ._types import TimeoutTypes
from ._types import VerifyTypes


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
        self.stubs = MappingsEndpoint(self.dispatcher)
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

    def __call__(  # type: ignore[return]
        self,
        *,
        method: str,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WiremockSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ) -> WiremockResponse:
        """Dispatches HTTP requests.  We could implement this via __call__ but it should be private."""
        if schema is not None:
            payload = schema(**schema_kw or {}).dump(payload)
        try:
            httpx_response = self.client.request(method=method, url=url, json=payload)
            print(httpx_response.request.content, httpx_response.request.url)
            status = httpx_response.status_code
            if status in (200, 201):
                # Successfully fetching/creating a resource.
                return WiremockResponse(httpx_response)
            elif status == 401:
                raise WiremockForbiddenException(httpx_response.text, status)
            elif status == 404:
                raise WiremockNotFoundException(
                    f"No wiremock instance running, {httpx_response.request.url} not found.", status
                )
            elif status == 422:
                raise WiremockMalformedRequest(httpx_response.text, status)
            elif status == 500:
                raise WiremockServerException(httpx_response.extensions["reason_phrase"], status)
        except httpx.TimeoutException as exc:
            raise WiremockTimeoutException(str(exc)) from None
        except httpx.ConnectError:
            raise WiremockConnectionException(self.host) from None
