import logging as log
import json
from os.path import join, dirname

from app.db import db_wrapper
from app.model import Product


contents_path = join(dirname(__file__), 'contents.json')


async def reset_products():
    await db_wrapper.db.drop_collection('product')
    log.debug('Products collection has been cleaned')

    with open(contents_path, 'r') as fd:
        contents = json.load(fd)

    async def fill_in():
        for data in contents:
            product = Product(**data)
            await product.commit()
        log.debug('Products collection was filled in')

    await fill_in()
