"""
Keep models and schemas tightly together to make future refactoring easier.
"""
import typing
from dataclasses import dataclass

from marshmallow import Schema
from marshmallow import fields
from marshmallow import validate


class WmSchema(Schema):
    """Todo: Custom error handling etc later."""


class ResponseDelay:
    """An abstract response delay."""

    type_ = fields.String(data_key="type")


class LogNormalSchema(WmSchema):
    median = fields.Integer()
    sigma = fields.Integer()
    type_ = fields.String(data_key="type", default="lognormal")


class UniformDelaySchema(WmSchema):
    lower = fields.Integer()
    upper = fields.Integer()
    type_ = fields.String(data_key="type", default="uniform")


class FixedDelaySchema(WmSchema):
    """Schema for setting global fixed delay across all stubs."""

    fixed_delay = fields.Integer(data_key="fixedDelay")


@dataclass(eq=True, frozen=True)
class FixedDelay:
    fixed_delay: int


class StubRequestSchema(WmSchema):
    """Schema for (de)serialising stub requests."""

    method = fields.String()
    url = fields.String()
    url_path = fields.String(data_key="urlPath")
    url_path_pattern = fields.String(data_key="urlPathPattern")
    url_pattern = fields.String(data_key="urlPattern")
    query_parameters = fields.Dict(data_key="queryParameters")
    headers = fields.Dict()
    basic_auth_credentials = fields.Dict(data_key="basicAuthCredentials")
    cookies = fields.Dict()
    body_patterns = fields.Dict(data_key="bodyPatterns")


@dataclass(eq=True, frozen=True)
class StubRequest:
    method: str
    url: str
    url_path: str
    url_path_pattern: str
    url_pattern: str
    query_parameters: typing.Dict[typing.Any, typing.Any]
    headers: typing.Dict[typing.Any, typing.Any]
    basic_auth_credentials: typing.Dict[typing.Any, typing.Any]
    cookies: typing.Dict[typing.Any, typing.Any]
    body_patterns: typing.Dict[typing.Any, typing.Any]


class _StubResponseContent(WmSchema):
    delay_distribution = fields.Nested(...)
    status = fields.Integer()
    status_message = fields.String(data_key="statusMessage")
    headers = fields.Dict()
    additional_proxy_request_headers = fields.Dict(data_key="additionalProxyRequestHeaders")
    # Todo: Only 1 of the following 3 can be specified; how does marshmallow handle that - validators?
    body = fields.String()
    base64_body = fields.String(data_key="base64Body")
    json_body = fields.String(data_key="jsonBody")
    body_file_name = fields.String(data_key="bodyFileName")
    fault = fields.String()
    fixed_delay_milliseconds = fields.Integer(data_key="fixedDelayMilliseconds")
    from_configure_stub = fields.Boolean(data_key="fromConfigureStub")
    proxy_base_url = fields.String(data_key="proxyBaseUrl")
    transformer_parameters = fields.Dict(data_key="transformersParameters")
    transformers = fields.List()


class StubResponseSchema(WmSchema):
    response = fields.Nested(_StubResponseContent)


class StubResponse:
    ...


class StubSchema(WmSchema):
    identity = fields.String(data_key="id")
    uuid = fields.String()
    name = fields.String()
    request = fields.Nested(StubRequestSchema)
    response = fields.Nested(StubResponseSchema)
    persistent = fields.Boolean()
    priority = fields.Integer(validate=validate.Range(min=1))
    scenario_name = fields.String(data_key="scenarioName")
    required_scenario_state = fields.String(data_key="requiredScenarioState")
    new_scenario_state = fields.String(data_key="newScenarioState")
    post_serve_actions = fields.Dict()
    metadata = fields.Dict()


@dataclass(eq=True, frozen=True)
class Stub:
    ...
