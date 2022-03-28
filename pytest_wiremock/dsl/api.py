class Then:
    """Response configurations."""

    def __init__(self) -> None:
        """Place holder"""


class When:
    """Request configurations."""

    def __init__(self) -> None:
        ...

    def then(self) -> Then:
        return Then()


class Given:
    """Pre configurations."""

    def __init__(self, verb: str):
        ...

    def when(self) -> When:
        return When()
