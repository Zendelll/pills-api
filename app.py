import asyncio
from aiohttp import web
from routes import setup_routes
import jinja2
import aiohttp_jinja2
from aiohttp.web_middlewares import middleware

app = web.Application()
setup_routes(app)

if __name__ == "__main__":
    web.run_app(app, host='::', port=8080)
       


