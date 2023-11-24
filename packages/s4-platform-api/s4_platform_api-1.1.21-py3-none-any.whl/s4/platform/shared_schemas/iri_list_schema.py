from marshmallow import fields
from s4.platform.internal.camel_case_schema import CamelCaseSchema


class IriListSchema(CamelCaseSchema):
    def __init__(self, **kwargs):
        super(IriListSchema, self).__init__(**kwargs)

    data = fields.List(fields.Str())
