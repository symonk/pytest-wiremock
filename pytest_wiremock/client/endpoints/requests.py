import httpx

from pytest_wiremock.client._constants import HTTPVerbs
from pytest_wiremock.client._protocols import DispatchCallable


class RequestsEndpoint:
    """
    Facade into requests.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def get_requests(self, limit: int, since: str) -> httpx.Response:
        """Retrieve all requests within limit that have been recorded as of since."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/requests", params={"limit": limit, "since": since})

    def delete_requests(self) -> httpx.Response:
        """Delete all the requests."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/requests")
