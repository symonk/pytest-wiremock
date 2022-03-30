import typing

from ._response import WiremockResponse
from ._schemas import WiremockSchema


class Requestable(typing.Protocol):
    def __call__(
        self,
        *,
        method: str,
        url: str,
        payload: typing.Optional[typing.Any] = None,
        params: typing.Optional[typing.Dict[str, typing.Any]] = None,
        schema: typing.Optional[typing.Type[WiremockSchema]] = None,
        schema_kw: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ) -> WiremockResponse:
        ...


class Queryable(typing.Protocol):
    def to_payload(self) -> typing.Dict[typing.Any, typing.Any]:
        ...
