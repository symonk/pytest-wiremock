class Given:
    """A builder for the wiremock client."""

    def __init__(self, verb: str, method_condition):
        self.verb = verb
        self.method_condition = method_condition()
