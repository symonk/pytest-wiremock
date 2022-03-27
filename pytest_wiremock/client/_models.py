import typing
import uuid

from pytest_wiremock.client._types import UuidTypes


class StubRequest:
    """Encapsulation of a stub mapping request."""

    def __init__(
        self,
        method: str,
        url: str,
        url_path: typing.Optional[str] = None,
        url_path_pattern: typing.Optional[str] = None,
        url_pattern: typing.Optional[str] = None,
        query_parameters: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        headers: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        body_patterns: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ) -> None:
        self.method = method
        self.url = url
        self.url_path = url_path
        self.url_path_pattern = url_path_pattern
        self.url_pattern = url_pattern
        self.query_parameters = query_parameters
        self.headers = headers
        self.body_patterns = body_patterns


class StubResponse:
    """Encapsulation of a stub mapping response."""

    def __init__(
        self,
        body: str,
        headers: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        transformers: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        fixed_delay_milliseconds: typing.Optional[int] = None,
        fault: typing.Optional[str] = None,
        from_configured_stub: bool = False,
        status_message: typing.Optional[str] = None,
        status: typing.Optional[int] = None,
    ) -> None:
        self.body = body
        self.headers = headers
        self.transformers = transformers
        self.fixed_delay_milliseconds = fixed_delay_milliseconds
        self.fault = fault
        self.from_configured_stub = from_configured_stub
        self.status_message = status_message
        self.status = status


class Stub:
    """
    An encapsulation of a stub mapping.
    """

    def __init__(
        self,
        request: StubRequest,
        response: StubResponse,
        id_: typing.Optional[str] = None,
        uuid_: typing.Optional[UuidTypes] = None,
        name: typing.Optional[str] = None,
        persistent: bool = False,
        priority: int = 1,
        scenario_name: typing.Optional[str] = None,
        required_scenario_state: typing.Optional[str] = None,
        new_scenario_state: typing.Optional[str] = None,
        post_serve_actions: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
        metadata: typing.Optional[typing.Dict[typing.Any, typing.Any]] = None,
    ) -> None:
        self.request = request
        self.response = response
        self.id_ = id_ or str(uuid.uuid4())
        self.uuid_ = uuid_
        self.name = name
        self.persistent = persistent
        self.priority = priority
        self.scenario_name = scenario_name
        self.required_scenario_state = required_scenario_state
        self.new_scenario_state = new_scenario_state
        self.post_serve_actions = post_serve_actions
        self.metadata = metadata


class FixedDelay:
    def __init__(self, fixed_delay: int) -> None:
        self.fixed_delay = fixed_delay
