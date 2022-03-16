import httpx

from .._decorators import handle_response
from .verbs import HTTPVerbs


class RequestsEndpoint:
    """
    Facade into requests.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def get_requests(self, limit: int, since: str) -> httpx.Response:
        """Retrieve all requests within limit that have been recorded as of since."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/requests", params={"limit": limit, "since": since})

    @handle_response(200)
    def delete_requests(self) -> httpx.Response:
        """Delete all the requests."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/requests")
