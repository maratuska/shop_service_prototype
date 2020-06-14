import logging as log
from typing import Optional, AsyncIterable

from app.model import Product, Fields


class Handler:

    def __init__(self, product: type(Product)):
        self._product = product

    async def create_product(self, product_data: dict) -> Optional[Product]:
        product = self._product(**product_data)
        await product.commit()
        return product

    async def find_product(self, data: dict) -> Optional[Product]:
        product = await self._product.find_one(data)
        return product

    async def find_products(self) -> AsyncIterable[Product]:
        return self._product.find({})

    async def filter_products(self, data: dict) -> AsyncIterable[Product]:
        filter_ = self._make_filter(data)
        return self._product.find(filter_)

    async def ensure_indexes(self):
        await self._product.ensure_indexes()

    @classmethod
    def _make_filter(cls, data, strict=True):
        operator = '$and' if strict else '$or'

        filter_ = {operator: [
            cls._make_name_filter(data),
            cls._make_params_filter(data),
        ]}
        log.debug(f'Filtering by {filter_}')

        return filter_

    @classmethod
    def _make_params_filter(cls, data: dict) -> dict:
        params_data = data.get(Fields.params)
        if params_data is None:
            params_filter = {}
        else:
            params_filter = {'$and': [
                {f'{Fields.params}.{name}': value}
                for name, value in params_data.items()
            ]}
        return params_filter

    @classmethod
    def _make_name_filter(cls, data: dict) -> dict:
        value = data.get(Fields.name)
        if value is not None:
            name_filter = {"$text": {"$search": value}}
        else:
            name_filter = {}
        return name_filter


handler = Handler(Product)
