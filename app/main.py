import logging as log
from aiohttp.web import Application, run_app

from app.service import handler, routes
from app.config import config
from app.db import db_wrapper
from app.contents import reset_products


def init_app():
    app = Application()
    app.router.add_routes(routes)

    app.on_startup.append(on_startup)
    app.on_cleanup.append(db_wrapper.close_mongo)

    return app


async def on_startup(app: Application):
    await db_wrapper.load_mongo(app)
    await reset_products()
    await handler.ensure_indexes()


def main():
    app = init_app()

    try:
        run_app(
            app,
            host=config.app_host,
            port=config.app_port,
        )
        log.info('Application is running')
    except OSError as exc:
        log.error('Run error', exc_info=exc)


if __name__ == "__main__":
    main()
