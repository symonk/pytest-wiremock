import ssl
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
