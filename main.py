import aiohttp
from aiohttp import web
async def app_factory():
    await pre_init()
    app = web.Application()
    app.router.add_get(...)
    return app

web.run_app(app_factory())
