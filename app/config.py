from typing import NamedTuple
from logging import basicConfig, INFO, DEBUG


basicConfig(
    level=INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)


class Config(NamedTuple):
    app_host: str = '127.0.0.1'
    app_port: int = 13031

    mongo_host: str = '127.0.0.1'
    mongo_port: int = 27017
    mongo_db_name: str = 'shop'

    mongo_addr: str = f'mongodb://{mongo_host}:{mongo_port}/{mongo_db_name}'


config = Config()
