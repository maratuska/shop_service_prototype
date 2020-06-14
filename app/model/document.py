from umongo import Document, fields
from pymongo import TEXT

from app.db import db_wrapper
from app.model import Fields, validators


@db_wrapper.instance.register
class Product(Document):

    # product barcode type
    product_id = fields.StringField(
        attribute=Fields.product_id,
        required=True,
        unique=True,
        validate=validators[Fields.product_id],
    )

    name = fields.StringField(
        attribute=Fields.name,
        required=True,
        validate=validators[Fields.name],
    )

    description = fields.StringField(
        attribute=Fields.description,
        default='Empty',
        validate=validators[Fields.description],
    )

    # max 100 parameters
    params = fields.ListField(
        fields.DictField(),
        attribute=Fields.params,
        validate=validators[Fields.params],
    )

    class Meta:
        strict = True
        collection_name = 'product'
        indexes = [
            [(Fields.name, TEXT)],
            Fields.params,
        ]
