import aiohttp
from aiohttp import web
async def oli(request):
  return web.Respones(text="ola puyo")

web.run_app(app)
