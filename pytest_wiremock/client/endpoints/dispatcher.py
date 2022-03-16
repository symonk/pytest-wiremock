import typing

import httpx

from .._exceptions import WiremockConnectionException
from .._exceptions import WiremockTimeoutException
from ..resources import WmSchema
from .verbs import HTTPVerbs


class Dispatcher:
    """
    Dispatch requests through the underlying client.
    """

    def __init__(self, client: httpx.Client, host: str) -> None:
        self.client = client
        self.host = host

    def post(
        self,
        *,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ):
        return self(method=HTTPVerbs.POST, **locals())

    def put(
        self,
        *,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ):
        return self(method=HTTPVerbs.PUT, **locals())

    def delete(
        self,
        *,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ):
        return self(method=HTTPVerbs.DELETE, **locals())

    def get(
        self,
        *,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WmSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ):
        return self(method=HTTPVerbs.GET, **locals())

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
        except httpx.TimeoutException as exc:
            raise WiremockTimeoutException(str(exc)) from None
        except httpx.ConnectError:
            raise WiremockConnectionException(self.host) from None
