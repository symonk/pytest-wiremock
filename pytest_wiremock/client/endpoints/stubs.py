import httpx

from pytest_wiremock.client._protocols import DispatchCallable
from pytest_wiremock.client.verbs import HTTPVerbs


class StubsEndpoint:
    """
    Facade into mappings.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def delete_all_stubs(self) -> httpx.Response:
        """Delete all registered stubs"""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    def reset_all_stubs(self) -> httpx.Response:
        """Reset all registered stubs to what is defined on disk in the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/reset")

    def save_stubs(self) -> httpx.Response:
        """Save all persistent stubs to the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/save")

    def delete_stub_with_uuid(self, uuid: str) -> httpx.Response:
        """Delete the stub with a matching uuid."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url=f"/mappings/delete/{uuid}")
