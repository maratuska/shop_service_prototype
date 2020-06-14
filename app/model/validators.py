from umongo import validate
from app.model import Fields

validators = {
    Fields.product_id: [
        validate.Regexp(
            r'\b\d{12,13}\b',
            error='Product barcode may be 12 or 13 digits'
        )
    ],
    Fields.name: [
        validate.Length(max=100),
    ],
    Fields.description: [
        validate.Length(max=1000),
    ],
    Fields.params: [
        validate.Length(max=100),
    ],
}
