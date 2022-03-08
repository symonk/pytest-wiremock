from marshmallow import Schema
from marshmallow import fields


class WmSchema(Schema):
    """Todo: Custom error handling etc later."""


class LogNormalSettingsSchema(WmSchema):
    """Schema for /settings"""

    median = fields.Integer()
    sigma = fields.Integer()
    type = fields.String(data_key="type", default="lognormal")
    fixed_delay = fields.Integer(data_key="fixedDelay")
