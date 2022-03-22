import httpx

from pytest_wiremock.client._protocols import DispatchCallable

from .._constants import HTTPVerbs


class ScenariosEndpoint:
    """
    Facade into scenarios.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def reset_scenarios(self) -> httpx.Response:
        """Reset the state of all scenarios."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/scenarios/reset")
