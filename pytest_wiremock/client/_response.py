import httpx


class WiremockResponse:
    """
    The response object for all calls to wiremock.
    """

    def __init__(self, delegate: httpx.Response) -> None:
        self.delegate = delegate

    def __getattr__(self, item: str):
        """Dynamic dispatch to the underlying response."""
        attr = getattr(self.delegate, item)
        if callable(item):

            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)

            return wrapper
        return attr
