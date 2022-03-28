from pytest_wiremock.client._protocols import Requestable


class RecordingsEndpoint:
    """
    Facade into recordings.
    """

    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher
