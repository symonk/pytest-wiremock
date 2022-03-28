from ._constants import HTTPVerbs
from ._protocols import Requestable
from ._response import WiremockResponse


class RequestsEndpoint:
    """
    Facade into requests.
    """

    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher

    def get_requests(self, limit: int, since: str) -> WiremockResponse:
        """Retrieve all requests within limit that have been recorded as of since."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/requests", params={"limit": limit, "since": since})

    def delete_requests(self) -> WiremockResponse:
        """Delete all the requests."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/requests")
