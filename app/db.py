import logging as log
from asyncio import get_event_loop
from aiohttp.web import Application
from umongo import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import config


class DBWrapper:
    def __init__(self, instance):
        self._instance = instance
        self._db = None

    async def load_mongo(self, app: Application):
        app['db'] = self.db
        log.debug('Mongo has been loaded')

    @classmethod
    async def close_mongo(cls, app: Application):
        db_ = app['db']
        db_.client.close()
        log.debug('Mongo has been closed')

    @property
    def instance(self):
        return self._instance

    @property
    def db(self):
        if self._db is None:
            self._init_db()

        return self._db

    def _init_db(self):
        connection = AsyncIOMotorClient(
            config.mongo_addr,
            io_loop=get_event_loop(),
        )
        self._db = connection.get_database()
        self._instance.init(self._db)


db_wrapper = DBWrapper(MotorAsyncIOInstance())
