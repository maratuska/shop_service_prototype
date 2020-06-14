import logging as log
from json import JSONDecodeError
from typing import Optional
from aiohttp import web
from aiohttp.web import Request
from marshmallow import UnmarshalResult
from pymongo.errors import OperationFailure
from umongo import ValidationError, Schema

from app.service import handler
from app.model import Product, FindProductSchema, FilterProductSchema


class Routes:

    def __init__(self):
        self._product_schema = Product.schema
        self._find_product_schema = FindProductSchema()
        self._filter_products_schema = FilterProductSchema()

    @classmethod
    async def _load_json(cls, request: Request):
        try:
            data = await request.json()
        except JSONDecodeError as exc:
            log.error('JSON decode error', exc_info=exc)
            raise web.HTTPBadRequest(reason=exc.msg,)
        else:
            return data

    def _deserialize(self, data: dict, schema: Optional[Schema] = None):
        schema = schema or self._product_schema
        try:
            result: UnmarshalResult = schema.load(data)
        except ValidationError as exc:
            log.error('Deserialization error', exc_info=exc)
            raise web.HTTPBadRequest(reason=exc.messages)
        else:
            return result.data

    async def set_product(self, request: Request):
        data = await self._load_json(request)
        data = self._deserialize(data)

        try:
            product: Product = await handler.create_product(data)
        except ValidationError as exc:
            log.error('Product creation error', exc_info=exc)
            raise web.HTTPBadRequest(reason=exc.messages)
        else:
            response = web.json_response(
                product.dump(),
                status=web.HTTPCreated.status_code,
            )
            return response

    async def get_product(self, request: Request):
        data = await self._load_json(request)
        data = self._deserialize(data, self._find_product_schema)

        product: Product = await handler.find_product(data)
        if product is None:
            log.warning('Product not found')
            raise web.HTTPNotFound(reason=data)

        response = web.json_response(
            product.dump(),
            status=web.HTTPOk.status_code,
        )
        return response

    @classmethod
    async def get_products(cls, _: Request):
        products = await handler.find_products()
        products = [product.dump() async for product in products]

        if not products:
            log.warning('Products not found')
            raise web.HTTPNotFound()

        response = web.json_response(
            products,
            status=web.HTTPOk.status_code,
        )
        return response

    async def filter_products(self, request: Request):
        data = await self._load_json(request)
        data = self._deserialize(data, self._filter_products_schema)

        products = await handler.filter_products(data)

        try:
            products = [product.dump() async for product in products]
        except OperationFailure as exc:
            log.error('Filtration error', exc.details['errmsg'])
            raise web.HTTPInternalServerError(reason=data)

        if not products:
            log.warning('Products not found')
            raise web.HTTPNotFound(reason=data)

        response = web.json_response(
            products,
            status=web.HTTPOk.status_code,
        )
        return response


routes_ = Routes()

routes = (
    web.get('/', routes_.get_products),
    web.get('/products', routes_.filter_products),
    web.get('/product', routes_.get_product),
    web.post('/product', routes_.set_product),
)
