from ._constants import HTTPVerbs
from ._models import FixedDelay
from ._protocols import Requestable
from ._response import WiremockResponse
from ._schemas import FixedDelaySchema


class SystemEndpoint:
    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher

    def set_fixed_delay(self, fixed_delay: int) -> WiremockResponse:
        """
        Configure a global fixed delay for all registered mappings. The response will not be returned
        until after this delay.

        :param fixed_delay: Number of milliseconds to wait before issuing the response.
        """
        return self.dispatcher(
            method=HTTPVerbs.POST, url="/settings", payload=FixedDelay(fixed_delay), schema=FixedDelaySchema
        )

    def reset(self) -> WiremockResponse:
        """Reset mappings to the default state and reset the request journal"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/reset")

    def shutdown(self) -> WiremockResponse:
        """Shutdown the wire mock instance"""
        return self.dispatcher(method=HTTPVerbs.POST, url="/shutdown")

    def get_settings(self) -> WiremockResponse:
        return self.dispatcher(method=HTTPVerbs.GET, url="/settings")
