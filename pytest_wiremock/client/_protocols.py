import typing

import httpx

from .resources import WmSchema


class DispatchCallable(typing.Protocol):
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
        ...
