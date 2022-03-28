import httpx

from pytest_wiremock._constants import HTTPVerbs
from pytest_wiremock._protocols import DispatchCallable

from ._models import FixedDelay
from ._schemas import FixedDelaySchema


class SystemEndpoint:
    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def set_fixed_delay(self, fixed_delay: int) -> httpx.Response:
        """
        Configure a global fixed delay for all registered stubs. The response will not be returned
        until after this delay.

        :param fixed_delay: Number of milliseconds to wait before issuing the response.
        """
        return self.dispatcher(
            method=HTTPVerbs.POST, url="/settings", payload=FixedDelay(fixed_delay), schema=FixedDelaySchema
        )

    def reset(self) -> httpx.Response:
        """Reset mappings to the default state and reset the request journal"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/reset")

    def shutdown(self) -> httpx.Response:
        """Shutdown the wire mock instance"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/shutdown")

    def get_settings(self) -> httpx.Response:
        return self.dispatcher(method=HTTPVerbs.GET, url="/settings")
