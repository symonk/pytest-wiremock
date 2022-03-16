from pytest_wiremock.client._protocols import DispatchCallable


class NearMissesEndpoint:
    """
    Facade into near misses.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher
