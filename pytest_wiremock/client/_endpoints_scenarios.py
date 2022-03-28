from ._constants import HTTPVerbs
from ._protocols import Requestable
from ._response import WiremockResponse


class ScenariosEndpoint:
    """
    Facade into scenarios.
    """

    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher

    def reset_scenarios(self) -> WiremockResponse:
        """Reset the state of all scenarios."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/scenarios/reset")
