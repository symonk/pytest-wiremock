import typing
import uuid

from ._constants import HTTPVerbs
from ._exceptions import ValidationException
from ._models import Mapping
from ._protocols import Requestable
from ._response import WiremockResponse
from ._schemas import StubSchema


class MappingsEndpoint:
    """
    Facade into mappings.
    """

    def __init__(self, dispatcher: Requestable) -> None:
        self.dispatcher = dispatcher

    def reset_stub_mappings(self) -> WiremockResponse:
        """Restore stub mappings to the defaults defined back in the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/reset")

    def save_stub_mappings(self) -> WiremockResponse:
        """Save all persistent stub mappings to the backing store."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings/save")

    def get_stub_with_mapping_id(self, stub_mapping_id: str) -> WiremockResponse:
        """Get stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.GET, url=f"/mappings/{stub_mapping_id}")

    def delete_stub_with_mapping_id(self, stub_mapping_id: str) -> WiremockResponse:
        """Delete stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.DELETE, url=f"/mappings/{stub_mapping_id}")

    def update_stub_with_mapping_id(self, stub_mapping_id: str) -> WiremockResponse:
        """Update stub mapping by uuid."""
        self._validate_uuid(stub_mapping_id)
        return self.dispatcher(method=HTTPVerbs.PUT, url=f"/mappings/{stub_mapping_id}")

    def create_stub(self, stub: Mapping) -> WiremockResponse:
        """creates a new stub mapping."""
        return self.dispatcher(method=HTTPVerbs.POST, url="/mappings", payload=stub, schema=StubSchema)

    def create_stubs(self, stubs: typing.Iterable[Mapping]) -> typing.List[WiremockResponse]:
        """Creates multiple mappings batch in one go.  (This is not an official wiremock API)."""
        return [self.create_stub(stub) for stub in stubs]

    def get_all_stubs(self, limit: int = 10, offset: int = 0) -> WiremockResponse:
        """Get all stub mappings."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/mappings", params={"limit": limit, "offset": offset})

    def delete_all_stubs(self) -> WiremockResponse:
        """Delete all stub mappings."""
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    def find_by_metadata(self, limit: int = 10, offset: int = 0) -> WiremockResponse:
        """Find mappings by matching on their metadata."""
        return self.dispatcher(method=HTTPVerbs.GET, url="/mappings", params={"limit": limit, "offset": offset})

    def remove_by_metadata(self) -> WiremockResponse:
        return self.dispatcher(method=HTTPVerbs.DELETE, url="/mappings")

    @staticmethod
    def _validate_uuid(_uuid: str) -> None:
        """Enforce the uuid is properly formatted and compliant."""
        try:
            uuid.UUID(_uuid)
        except ValueError:
            raise ValidationException(f"uuid={_uuid} is not a valid uuid.") from None
