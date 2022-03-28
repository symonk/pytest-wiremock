from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPVerbs:
    """
    HTTP Verbs used by wiremock.  Currently, only the 4 verbs below are utilised by
    their API.
    """

    POST = "POST"
    GET = "GET"
    DELETE = "DELETE"
    PUT = "PUT"


@dataclass(frozen=True)
class ConnectionLiterals:
    """Fault connection literals."""

    CONNECTION_RESET_BY_PEER: str = "CONNECTION_RESET_BY_PEER"
    EMPTY_RESPONSE: str = "EMPTY_RESPONSE"
    MALFORMED_RESPONSE_CHUNK: str = "MALFORMED_RESPONSE_CHUNK"
    RANDOM_DATA_THEN_CLOSE: str = "RANDOM_DATA_THEN_CLOSE"
