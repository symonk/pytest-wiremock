"""
Keep models and schemas tightly together to make future refactoring easier.
"""

from dataclasses import dataclass

from marshmallow import Schema
from marshmallow import fields


class WmSchema(Schema):
    """Todo: Custom error handling etc later."""


class FixedDelaySchema(WmSchema):
    """Schema for setting global fixed delay across all stubs."""

    fixed_delay = fields.Integer(data_key="fixedDelay")


@dataclass(eq=True, frozen=True)
class FixedDelay:
    fixed_delay: int
