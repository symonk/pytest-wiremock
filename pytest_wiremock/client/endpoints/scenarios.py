import httpx

from .._decorators import handle_response


class ScenariosEndpoint:
    """
    Facade into scenarios.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def reset_scenarios(self) -> httpx.Response:
        """Reset the state of all scenarios."""
        return self.dispatcher.post(url="/scenarios/reset")
