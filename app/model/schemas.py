from umongo import Schema, fields
from app.model import Product, Fields, validators


class FindProductSchema(Product.schema.as_marshmallow_schema()):
    class Meta:
        strict = True
        fields = (Fields.product_id, )


class FilterProductSchema(Schema):
    name = fields.StringField(
        required=False,
        validate=validators[Fields.name]
    )
    params = fields.DictField(
        required=False,
        validate=validators[Fields.params]
    )

    class Meta:
        strict = True
