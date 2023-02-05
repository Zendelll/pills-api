import asyncio
from aiohttp import web
from routes import setup_routes
import jinja2
import aiohttp_jinja2
from aiohttp.web_middlewares import middleware

#docker build -t test-api /Users/zendell/test-api
#docker run -p 8080:8080 test-api

app = web.Application()
setup_routes(app)

if __name__ == "__main__":
    web.run_app(app)
       


