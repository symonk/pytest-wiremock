import httpx

from .._decorators import handle_response
from .verbs import HTTPVerbs


class StubsEndpoint:
    """
    Facade into mappings.
    """

    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher

    @handle_response(200)
    def delete_all_stubs(self) -> httpx.Response:
        """Delete all registered stubs"""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    @handle_response(200)
    def reset_all_stubs(self) -> httpx.Response:
        """Reset all registered stubs to what is defined on disk in the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/reset")

    @handle_response(200)
    def save_stubs(self) -> httpx.Response:
        """Save all persistent stubs to the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/save")

    @handle_response(200)
    def delete_stub_with_uuid(self, uuid: str) -> httpx.Response:
        """Delete the stub with a matching uuid."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url=f"/mappings/delete/{uuid}")
