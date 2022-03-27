import httpx

from pytest_wiremock._constants import HTTPVerbs
from pytest_wiremock._protocols import DispatchCallable


class ScenariosEndpoint:
    """
    Facade into scenarios.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def reset_scenarios(self) -> httpx.Response:
        """Reset the state of all scenarios."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/scenarios/reset")
