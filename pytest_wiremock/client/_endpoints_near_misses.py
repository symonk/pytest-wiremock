from pytest_wiremock.client._protocols import Requestable


class NearMissesEndpoint:
    """
    Facade into near misses.
    """

    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher
