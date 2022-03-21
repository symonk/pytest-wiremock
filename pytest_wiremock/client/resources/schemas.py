import typing

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import post_load
from marshmallow import validate


class WmSchema(Schema):
    """Todo: Custom error handling etc later."""

    @staticmethod
    def drop_nones(data: typing.Dict[typing.Any, typing.Any]) -> typing.Dict[typing.Any, typing.Any]:
        """Drop keys with a `None` value from the serialised data before sending it across."""
        return {k: v for k, v in data.items() if v is not None}


class LogNormalSchema(WmSchema):
    median = fields.Integer()
    sigma = fields.Integer()
    type_ = fields.String(data_key="type", default="lognormal")


class FixedDelaySchema(WmSchema):
    """Schema for setting global fixed delay across all stubs."""

    fixed_delay = fields.Integer(data_key="fixedDelay")


class UniformDelaySchema(WmSchema):
    lower = fields.Integer()
    upper = fields.Integer()
    type_ = fields.String(data_key="type", default="uniform")


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

    @post_dump
    def clean_request_schema(self, data, *args, **kwargs):
        return self.drop_nones(data)


class StubResponseContentSchema(WmSchema):
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
    transformers = fields.List(fields.String())

    @post_dump
    def clean_response_schema(self, data, *args, **kwargs):
        return self.drop_nones(data)


class StubSchema(WmSchema):
    id_ = fields.String(data_key="id")
    uuid = fields.String()
    name = fields.String()
    request = fields.Nested(StubRequestSchema())
    response = fields.Nested(StubResponseContentSchema())
    persistent = fields.Boolean()
    priority = fields.Integer(validate=validate.Range(min=1))
    scenario_name = fields.String(data_key="scenarioName")
    required_scenario_state = fields.String(data_key="requiredScenarioState")
    new_scenario_state = fields.String(data_key="newScenarioState")
    post_serve_actions = fields.Dict()
    metadata = fields.Dict()

    @post_load
    def create_stub(self, *args, **kwargs):
        ...

    @post_dump
    def clean_stub_schema(self, data, many: bool, **kwargs):
        """Drop `None` value(s) when serialising a stub mapping."""
        return self.drop_nones(data)


class ResponseDelay:
    """An abstract response delay."""

    type_ = fields.String(data_key="type")
