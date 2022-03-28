import uuid

import httpx

from pytest_wiremock._constants import HTTPVerbs
from pytest_wiremock._protocols import DispatchCallable
from pytest_wiremock.client._models import Stub
from pytest_wiremock.client._schemas import StubSchema
from .._exceptions import ValidationException


class MappingsEndpoint:
    """
    Facade into mappings.
    """

    def __init__(self, dispatcher: DispatchCallable) -> None:
        self.dispatcher = dispatcher

    def reset_stub_mappings(self) -> httpx.Response:
        """Restore stub mappings to the defaults defined back in the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/reset")

    def save_stub_mappings(self) -> httpx.Response:
        """Save all persistent stub mappings to the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/save")

    def get_stub_with_mapping_id(self, stub_mapping_id: str) -> httpx.Response:
        """Get stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.GET, url=f"/mappings/{stub_mapping_id}")

    def delete_stub_with_mapping_id(self, stub_mapping_id: str) -> httpx.Response:
        """Delete stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.DELETE, url=f"/mappings/{stub_mapping_id}")

    def update_stub_with_mapping_id(self, stub_mapping_id: str) -> httpx.Response:
        """Update stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.PUT, url=f"/mappings/{stub_mapping_id}")

    def create_stub(self, stub: Stub) -> httpx.Response:
        """creates a new stub mapping."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings", payload=stub, schema=StubSchema)

    def get_all_stubs(self, limit: int = 10, offset: int = 0) -> httpx.Response:
        """Get all stub mappings."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/mappings", params={"limit": limit, "offset": offset})

    def delete_all_stubs(self) -> httpx.Response:
        """Delete all stub mappings."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    def find_by_metadata(self, limit: int = 10, offset: int = 0) -> httpx.Response:
        """Find stubs by matching on their metadata."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/mappings", params={"limit": limit, "offset": offset})

    def remove_by_metadata(self) -> httpx.Response:
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    @staticmethod
    def _validate_uuid(_uuid: str) -> None:
        """ Enforce the uuid is properly formatted and compliant."""
        try:
            uuid.UUID(_uuid)
        except ValueError:
            raise ValidationException(f"uuid={_uuid} is not a valid uuid.") from None
