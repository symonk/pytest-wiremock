class NearMissesEndpoint:
    """
    Facade into near misses.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher
