from __future__ import annotations

import typing
from types import TracebackType

import httpx

from ._types import TimeoutTypes
from ._types import VerifyTypes
from .endpoints import Dispatcher
from .endpoints import NearMissesEndpoint
from .endpoints import RecordingsEndpoint
from .endpoints import RequestsEndpoint
from .endpoints import ScenariosEndpoint
from .endpoints import StubsEndpoint
from .endpoints import SystemEndpoint


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
        dispatcher: typing.Callable[[httpx.Client, str], httpx.Response] = Dispatcher,
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
