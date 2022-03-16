class RecordingsEndpoint:
    """
    Facade into recordings.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher
