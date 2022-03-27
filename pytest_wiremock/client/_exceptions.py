import typing


class WiremockApiException(Exception):
    """Base class for pytest-wiremock exceptions."""

    def __init__(self, message: typing.Optional[str] = None, status_code: typing.Optional[int] = None, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code


class WiremockTimeoutException(WiremockApiException):
    """Raised when the underlying httpx client times out on either connect, read, write or pool."""


class WiremockConnectionException(WiremockApiException):
    """Raised when an attempt to connect to a running wiremock instance failed."""

    def __init__(self, host: str) -> None:
        super().__init__(f"Unable to connect to a wiremock instance running on: {host}")


class WiremockForbiddenException(WiremockApiException):
    """Raised when wiremock returns a 401 forbidden."""


class WiremockNotFoundException(WiremockApiException):
    """Raised when wiremock returns a 404 not found."""


class WiremockMalformedRequest(WiremockApiException):
    """Raised when the dispatched requests do not conform to the servers schema and general standards."""


class WiremockServerException(WiremockApiException):
    """Raised when the wiremock server responds with a 500.  Often when an invalid/missing payload is sent."""
