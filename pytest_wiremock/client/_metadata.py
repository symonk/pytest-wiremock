import typing

from ._protocols import Queryable


class MatchingJsonPath(Queryable):
    def __init__(self, expression: str, contains: str) -> None:
        self.expression = expression
        self.contains = contains

    def to_payload(self) -> typing.Dict[typing.Any, typing.Any]:
        return {"matchesJsonPath": self.__dict__}
