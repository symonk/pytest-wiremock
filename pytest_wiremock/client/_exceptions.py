import typing


class WiremockApiException(Exception):
    """Base class for pytest-wiremock exceptions."""

    status_code: typing.Optional[int] = None

    def __init__(self, status_code: typing.Optional[int] = None, message: typing.Optional[str] = None, *args, **kwargs):
        super(message, *args, **kwargs)
        self.status_code = status_code


class WiremockTimeoutException(WiremockApiException):
    """Raised when the underlying httpx client times out on either connect, read, write or pool."""

    ...


class WiremockConnectionException(WiremockApiException):
    """Raised when an attempt to connect to a running wiremock instance failed."""

    def __init__(self, host: str) -> None:
        super().__init__(message=f"Unable to connect to a wiremock instance running on: {host}")
