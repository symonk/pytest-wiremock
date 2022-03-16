import httpx

from .._decorators import handle_response
from ..resources import FixedDelay
from ..resources import FixedDelaySchema
from .dispatcher import Dispatcher
from .verbs import HTTPVerbs


class SystemEndpoint:
    def __init__(self, dispatcher: Dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def set_fixed_delay(self, fixed_delay: int) -> httpx.Response:
        """
        Configure a global fixed delay for all registered stubs. The response will not be returned
        until after this delay.

        :param fixed_delay: Number of milliseconds to wait before issuing the response.
        """
        return self.dispatcher(
            method=HTTPVerbs.POST, url="/settings", payload=FixedDelay(fixed_delay), schema=FixedDelaySchema
        )

    @handle_response(200)
    def reset(self) -> httpx.Response:
        """Reset mappings to the default state and reset the request journal"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/reset")

    @handle_response(200)
    def shutdown(self) -> httpx.Response:
        """Shutdown the wire mock instance"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/shutdown")

    @handle_response(200)
    def get_settings(self) -> httpx.Response:
        return self.dispatcher(method=HTTPVerbs.GET, url="/settings")
