from pytest_wiremock.client._protocols import DispatchCallable


class RecordingsEndpoint:
    """
    Facade into recordings.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher
