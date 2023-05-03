import asyncio
from aiohttp import web
from internal.logger import logger
from routes import setup_routes
import jinja2
import aiohttp_jinja2
from aiohttp.web_middlewares import middleware



#docker build -t test-api /Users/zendell/test-api
#docker run -p 8080:8080 -v /Users/zendell/test-api/db/:/usr/src/app/db test-api

app = web.Application()
setup_routes(app)

if __name__ == "__main__":
    logger.info("Api app started")
    web.run_app(app)
    
       


