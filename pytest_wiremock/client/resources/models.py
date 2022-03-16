import typing
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class FixedDelay:
    fixed_delay: int


@dataclass(eq=True, frozen=True)
class StubRequest:
    method: str
    url: str
    url_path: str
    url_path_pattern: str
    url_pattern: str
    query_parameters: typing.Dict[typing.Any, typing.Any]
    headers: typing.Dict[typing.Any, typing.Any]
    basic_auth_credentials: typing.Dict[typing.Any, typing.Any]
    cookies: typing.Dict[typing.Any, typing.Any]
    body_patterns: typing.Dict[typing.Any, typing.Any]


class StubResponse:
    ...


@dataclass(eq=True, frozen=True)
class Stub:
    ...
