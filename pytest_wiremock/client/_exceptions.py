class WiremockException(Exception):
    """Base class for pytest-wiremock exceptions."""


class WiremockConnectionError(WiremockException):
    """Raised when an attempt to connect to a running wiremock instance failed."""

    def __init__(self, host: str) -> None:
        super().__init__(f"Unable to connect to a wiremock instance running on: {host}")
