import ssl
import typing
import uuid
from typing import Optional
from typing import Tuple
from typing import Union

from httpx import Timeout

TimeoutTypes = Union[
    Optional[float],
    Tuple[Optional[float], Optional[float], Optional[float], Optional[float]],
    Timeout,
]
VerifyTypes = Union[str, bool, ssl.SSLContext]

UuidTypes = Union[str, uuid.UUID]


FaultTypes = typing.Optional[
    typing.Literal["CONNECTION_RESET_BY_PEER", "EMPTY_RESPONSE", "MALFORMED_RESPONSE_CHUNK", "RANDOM_DATA_THEN_CLOSE"]
]
